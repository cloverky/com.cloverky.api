from __future__ import annotations

from abc import ABC, abstractmethod

from vision.app.dtos.face_train_dto import FaceTrainCommand, FaceTrainResult


class YoloPort(ABC):
    @abstractmethod
    async def train(self, command: FaceTrainCommand) -> FaceTrainResult:
        """YOLO 모델을 파인튜닝하고 결과를 반환한다."""
        pass

    @abstractmethod
    async def detect(self, image_path: str, model_path: str) -> list[dict]:
        """학습된 모델로 이미지에서 얼굴을 감지한다."""
        pass
