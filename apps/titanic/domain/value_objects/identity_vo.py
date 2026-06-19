from __future__ import annotations
import re
from dataclasses import dataclass
from typing import Optional

from titanic.domain.value_objects.gender_vo import Gender
from titanic.domain.value_objects.title_vo import Title

_TITLE_RE = re.compile(r"([A-Za-z]+)\.")


@dataclass(frozen=True)
class PassengerIdentity:
    """성별과 호칭을 묶는 임베디드 VO.

    Gender↔Title +0.45 — 두 피처가 동일한 '사회적 정체성'을 표현.
    """
    gender: Gender
    title: Title

    @classmethod
    def from_raw(cls, gender: Optional[str], name: Optional[str]) -> "PassengerIdentity":
        match = _TITLE_RE.search(name or "")
        extracted = match.group(1) if match else None
        return cls(
            gender=Gender.from_raw(gender),
            title=Title.from_raw(extracted),
        )

    @property
    def is_female(self) -> bool:
        return self.gender.is_female

    @property
    def is_consistent(self) -> bool:
        """성별과 호칭이 일치하는지 검증 (데이터 품질 체크)."""
        return self.gender.is_female == self.title.is_female

    def __str__(self) -> str:
        return f"{self.title} ({self.gender})"
