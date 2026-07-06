from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class GenderType(str, Enum):
    MALE = "male"
    FEMALE = "female"


@dataclass(frozen=True)
class Gender:
    value: GenderType

    @classmethod
    def from_raw(cls, raw: str | None) -> Gender:
        if raw is None or raw.strip() == "":
            raise ValueError("성별은 필수 값입니다.")
        normalized = raw.strip().lower()
        try:
            return cls(value=GenderType(normalized))
        except ValueError:
            raise ValueError(
                f"성별은 'male' 또는 'female' 이어야 합니다. 입력값: {raw!r}"
            )

    @property
    def is_female(self) -> bool:
        return self.value == GenderType.FEMALE

    @property
    def is_male(self) -> bool:
        return self.value == GenderType.MALE

    def __str__(self) -> str:
        return self.value.value
