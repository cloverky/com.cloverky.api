from __future__ import annotations

import os
from pathlib import Path

from vision.app.ports.output.face_dataset_port import FaceDatasetPort

_DEFAULT_YAML = (
    Path(__file__).resolve().parents[4] / "resources" / "yolo_train" / "data.yaml"
)


class LocalYoloDatasetAdapter(FaceDatasetPort):
    def __init__(self, yaml_path: str | None = None) -> None:
        self._yaml_path = Path(yaml_path) if yaml_path else _DEFAULT_YAML

    def get_dataset_config_path(self) -> str:
        if not self._yaml_path.exists():
            raise FileNotFoundError(f"YOLO data.yaml 없음: {self._yaml_path}")
        return str(self._yaml_path)
