from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class TitleType(int, Enum):
    UNKNOWN = 0
    MR     = 1
    MISS   = 2
    MRS    = 3
    MASTER = 4
    ROYAL  = 5
    RARE   = 6


_RARE  = {"Capt", "Col", "Don", "Dr", "Major", "Rev", "Jonkheer", "Dona", "Mme"}
_ROYAL = {"Countess", "Lady", "Sir"}
_NORM  = {"Mlle": TitleType.MR, "Ms": TitleType.MISS,
          "Mr": TitleType.MR, "Miss": TitleType.MISS,
          "Mrs": TitleType.MRS, "Master": TitleType.MASTER}


@dataclass(frozen=True)
class Title:
    value: TitleType

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> "Title":
        if raw is None or raw.strip() == "":
            return cls(value=TitleType.UNKNOWN)
        t = raw.strip()
        if t in _RARE:
            return cls(value=TitleType.RARE)
        if t in _ROYAL:
            return cls(value=TitleType.ROYAL)
        return cls(value=_NORM.get(t, TitleType.UNKNOWN))

    @property
    def encoded(self) -> int:
        return self.value.value

    @property
    def is_female(self) -> bool:
        return self.value in {TitleType.MISS, TitleType.MRS}

    def __str__(self) -> str:
        return self.value.name.capitalize()
