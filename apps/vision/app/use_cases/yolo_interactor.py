from __future__ import annotations

import asyncio
import logging
from pathlib import Path

from ultralytics import YOLO

from vision.app.dtos.face_train_dto import FaceTrainCommand, FaceTrainResult
from vision.app.ports.output.face_dataset_port import FaceDatasetPort
from vision.app.ports.output.yolo_port import YoloPort

logger = logging.getLogger(__name__)

# 지원 모델 — 가벼운 순
SUPPORTED_MODELS = {
    "yolo11n": "yolo11n.pt",   # 1순위: 최신 초경량 (2.6M params)
    "yolov8n": "yolov8n.pt",   # 2순위: 안정적 호환 (3.2M params)
}


class YoloInteractor(YoloPort):
    def __init__(self, dataset_port: FaceDatasetPort) -> None:
        self._dataset_port = dataset_port

    # ──────────────────────────────────────────────
    # Train
    # ──────────────────────────────────────────────
    async def train(self, command: FaceTrainCommand) -> FaceTrainResult:
        dataset_yaml = self._dataset_port.get_dataset_config_path()
        logger.info(
            "[YOLO] 파인튜닝 시작 — model=%s epochs=%d batch=%d",
            command.model_name, command.epochs, command.batch_size,
        )

        def _run() -> tuple[str, dict]:
            model = YOLO(command.model_name)
            results = model.train(
                data=dataset_yaml,
                epochs=command.epochs,
                batch=command.batch_size,
                imgsz=command.imgsz,
                device=command.device,
                name="face_finetune",
            )
            best = Path(results.save_dir) / "weights" / "best.pt"
            metrics = {
                "mAP50":    round(float(results.results_dict.get("metrics/mAP50(B)", 0)), 4),
                "mAP50-95": round(float(results.results_dict.get("metrics/mAP50-95(B)", 0)), 4),
                "precision": round(float(results.results_dict.get("metrics/precision(B)", 0)), 4),
                "recall":    round(float(results.results_dict.get("metrics/recall(B)", 0)), 4),
            }
            return str(best), metrics

        try:
            best_path, metrics = await asyncio.to_thread(_run)
            logger.info("[YOLO] 파인튜닝 완료 — best=%s %s", best_path, metrics)
            return FaceTrainResult(success=True, best_model_path=best_path, metrics=metrics)
        except Exception as e:
            logger.error("[YOLO] 파인튜닝 실패 — %s", e)
            return FaceTrainResult(success=False, best_model_path="", metrics={"error": str(e)})

    # ──────────────────────────────────────────────
    # Detect
    # ──────────────────────────────────────────────
    async def detect(self, image_path: str, model_path: str = "yolo11n.pt") -> list[dict]:
        def _run() -> list[dict]:
            model = YOLO(model_path)
            results = model(image_path, verbose=False)
            detections: list[dict] = []
            for r in results:
                for box in r.boxes:
                    detections.append({
                        "label":      model.names[int(box.cls[0])],
                        "confidence": round(float(box.conf[0]), 4),
                        "bbox":       [round(v, 2) for v in box.xyxy[0].tolist()],
                    })
            return detections

        return await asyncio.to_thread(_run)
