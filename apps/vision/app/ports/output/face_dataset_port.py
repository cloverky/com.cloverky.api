from __future__ import annotations

from abc import ABC, abstractmethod


class FaceDatasetPort(ABC):
    @abstractmethod
    def get_dataset_config_path(self) -> str:
        """YOLO 학습에 필요한 data.yaml 파일의 절대 경로를 반환한다."""
        pass
