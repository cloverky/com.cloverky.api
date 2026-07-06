from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class FaceTrainCommand:
    epochs: int = 10
    batch_size: int = 8
    imgsz: int = 640
    device: str = "0"
    model_name: str = "yolo11n.pt"


@dataclass(frozen=True)
class FaceTrainResult:
    success: bool
    best_model_path: str
    metrics: dict = field(default_factory=dict)
