from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class SurvivalResult(int, Enum):
    DIED = 0
    SURVIVED = 1


@dataclass(frozen=True)
class SurvivalStatus:
    value: Optional[SurvivalResult]

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> "SurvivalStatus":
        if raw is None or str(raw).strip() == "":
            return cls(value=None)
        mapping: dict[str, SurvivalResult] = {
            "0": SurvivalResult.DIED, "false": SurvivalResult.DIED, "no": SurvivalResult.DIED,
            "1": SurvivalResult.SURVIVED, "true": SurvivalResult.SURVIVED, "yes": SurvivalResult.SURVIVED,
        }
        normalized = str(raw).strip().lower()
        if normalized not in mapping:
            raise ValueError(f"생존 여부는 0/1 이어야 합니다. 입력값: {raw!r}")
        return cls(value=mapping[normalized])

    @property
    def is_unknown(self) -> bool:
        return self.value is None

    @property
    def survived(self) -> bool:
        return self.value == SurvivalResult.SURVIVED

    def __str__(self) -> str:
        if self.value is None:
            return "unknown"
        return "생존" if self.survived else "사망"
