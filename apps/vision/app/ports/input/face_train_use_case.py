from __future__ import annotations

from abc import ABC, abstractmethod

from vision.app.dtos.face_train_dto import FaceTrainCommand, FaceTrainResult


class FaceTrainUseCase(ABC):
    @abstractmethod
    async def train(self, command: FaceTrainCommand) -> FaceTrainResult:
        """얼굴 인식 YOLO 모델을 파인튜닝한다."""
        pass

    @abstractmethod
    async def detect(self, image_path: str) -> list[dict]:
        """이미지에서 얼굴을 감지하고 결과를 반환한다."""
        pass
