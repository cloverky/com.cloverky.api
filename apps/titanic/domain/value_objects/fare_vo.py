from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class FareBand(int, Enum):
    VERY_LOW = 1
    LOW = 2
    HIGH = 3
    VERY_HIGH = 4


@dataclass(frozen=True)
class Fare:
    value: float

    @classmethod
    def from_raw(cls, raw: str | float | None) -> Fare:
        if raw is None or str(raw).strip() == "":
            return cls(value=0.0)
        try:
            val = float(str(raw).strip())
        except ValueError:
            raise ValueError(f"운임은 숫자여야 합니다. 입력값: {raw!r}")
        if val < 0:
            raise ValueError("운임은 0 이상이어야 합니다.")
        return cls(value=val)

    @property
    def is_free(self) -> bool:
        return self.value == 0.0

    @property
    def band(self) -> FareBand:
        if self.value <= 7.91:
            return FareBand.VERY_LOW
        if self.value <= 14.45:
            return FareBand.LOW
        if self.value <= 31.0:
            return FareBand.HIGH
        return FareBand.VERY_HIGH

    def __str__(self) -> str:
        return f"{self.value:.2f}"
