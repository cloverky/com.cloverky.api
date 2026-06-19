from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Parch:
    value: int

    @classmethod
    def from_raw(cls, raw: Optional[str | int]) -> "Parch":
        if raw is None or str(raw).strip() == "":
            return cls(value=0)
        try:
            val = int(str(raw).strip())
        except ValueError:
            raise ValueError(f"Parch는 정수여야 합니다. 입력값: {raw!r}")
        if val < 0:
            raise ValueError("Parch는 0 이상이어야 합니다.")
        return cls(value=val)

    @property
    def has_parent_or_child(self) -> bool:
        return self.value > 0

    def __str__(self) -> str:
        return str(self.value)
