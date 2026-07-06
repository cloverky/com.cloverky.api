from __future__ import annotations

import asyncio
import logging

from ultralytics import YOLO

from vision.app.dtos.face_train_dto import FaceTrainCommand, FaceTrainResult
from vision.app.ports.input.face_train_use_case import FaceTrainUseCase
from vision.app.ports.output.face_dataset_port import FaceDatasetPort

logger = logging.getLogger(__name__)


class FaceTrainInteractor(FaceTrainUseCase):
    def __init__(self, dataset_port: FaceDatasetPort) -> None:
        self._dataset_port = dataset_port

    async def train(self, command: FaceTrainCommand) -> FaceTrainResult:
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
            model = YOLO("yolo11n-face.pt")
            results = model(image_path)
            detections = []
            for r in results:
                for box in r.boxes:
                    detections.append({
                        "label": model.names[int(box.cls[0])],
                        "confidence": round(float(box.conf[0]), 4),
                        "bbox": box.xyxy[0].tolist(),
                    })
            return detections

        return await asyncio.to_thread(_run_detect)
