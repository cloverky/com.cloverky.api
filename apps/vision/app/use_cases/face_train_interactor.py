from __future__ import annotations

import asyncio
import logging
from pathlib import Path

import torch
import torch.nn.functional as F
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image

from vision.app.dtos.face_train_dto import FaceTrainCommand, FaceTrainResult
from vision.app.ports.input.face_train_use_case import FaceTrainUseCase
from vision.app.ports.output.face_dataset_port import FaceDatasetPort

logger = logging.getLogger(__name__)

_TRAIN_DIR = Path(__file__).resolve().parents[2] / "resourecs" / "yolo_train" / "train"

_mtcnn: MTCNN | None = None
_resnet: InceptionResnetV1 | None = None
_db: list[tuple[str, torch.Tensor]] = []  # [(label, embedding)]


def _get_models() -> tuple[MTCNN, InceptionResnetV1]:
    global _mtcnn, _resnet
    if _mtcnn is None:
        _mtcnn = MTCNN(image_size=160, keep_all=False, post_process=True)
    if _resnet is None:
        _resnet = InceptionResnetV1(pretrained="vggface2").eval()
    return _mtcnn, _resnet


def _build_db(mtcnn: MTCNN, resnet: InceptionResnetV1) -> list[tuple[str, torch.Tensor]]:
    db: list[tuple[str, torch.Tensor]] = []
    for label_dir in sorted(_TRAIN_DIR.iterdir()):
        if not label_dir.is_dir():
            continue
        label = label_dir.name.replace("_", " ").title()
        for img_path in list(label_dir.glob("*.jpg"))[:5]:  # 클래스당 최대 5장
            try:
                img = Image.open(img_path).convert("RGB")
                face = mtcnn(img)
                if face is None:
                    continue
                with torch.no_grad():
                    emb = resnet(face.unsqueeze(0)).squeeze(0)
                db.append((label, emb))
            except Exception:
                continue
    return db


class FaceTrainInteractor(FaceTrainUseCase):
    def __init__(self, dataset_port: FaceDatasetPort) -> None:
        self._dataset_port = dataset_port

    async def train(self, command: FaceTrainCommand) -> FaceTrainResult:
        from ultralytics import YOLO
        dataset_yaml = self._dataset_port.get_dataset_config_path()
        logger.info("[Vision] 파인튜닝 시작 — yaml=%s epochs=%d", dataset_yaml, command.epochs)

        def _run_train() -> tuple[str, dict]:
            model = YOLO(command.model_name)
            results = model.train(
                data=dataset_yaml,
                epochs=command.epochs,
                batch=command.batch_size,
                imgsz=command.imgsz,
                device=command.device,
            )
            best_path = str(results.save_dir / "weights" / "best.pt")
            metrics = {
                "mAP50": float(results.results_dict.get("metrics/mAP50(B)", 0)),
                "mAP50-95": float(results.results_dict.get("metrics/mAP50-95(B)", 0)),
            }
            return best_path, metrics

        best_path, metrics = await asyncio.to_thread(_run_train)
        logger.info("[Vision] 파인튜닝 완료 — best=%s metrics=%s", best_path, metrics)
        return FaceTrainResult(success=True, best_model_path=best_path, metrics=metrics)

    async def detect(self, image_path: str) -> list[dict]:
        def _run_detect() -> list[dict]:
            global _db
            try:
                mtcnn, resnet = _get_models()
                if not _db:
                    logger.info("[Vision] 얼굴 DB 구축 중…")
                    _db = _build_db(mtcnn, resnet)
                    logger.info("[Vision] DB 완료 — %d 개 임베딩", len(_db))

                img = Image.open(image_path).convert("RGB")
                face = mtcnn(img)
                if face is None:
                    return []

                with torch.no_grad():
                    query_emb = resnet(face.unsqueeze(0)).squeeze(0)

                # 코사인 유사도로 가장 가까운 셀럽 찾기
                scores: dict[str, float] = {}
                for label, db_emb in _db:
                    sim = float(F.cosine_similarity(query_emb.unsqueeze(0), db_emb.unsqueeze(0)))
                    if label not in scores or sim > scores[label]:
                        scores[label] = sim

                if not scores:
                    return []

                # 상위 1개만 반환
                best_label = max(scores, key=lambda k: scores[k])
                best_score = scores[best_label]
                confidence = round(max(0.0, (best_score + 1) / 2), 4)  # [-1,1] → [0,1]

                return [{"label": best_label, "confidence": confidence, "bbox": []}]
            except Exception as e:
                logger.warning("[Vision] 얼굴 인식 실패 — %s", e)
                return []

        return await asyncio.to_thread(_run_detect)
