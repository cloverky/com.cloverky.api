from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from titanic.domain.value_objects.pclass_vo import PClass, PClassType
from titanic.domain.value_objects.fare_vo import Fare
from titanic.domain.value_objects.cabin_vo import Cabin


@dataclass(frozen=True)
class ClassInfo:
    """티켓 등급·운임·객실을 묶는 임베디드 VO.

    PClass↔Fare -0.63 / PClass↔Cabin -0.57 / Fare↔Cabin +0.40
    세 피처가 동일한 '사회적 계층/좌석' 개념을 표현.
    """
    pclass: PClass
    fare: Fare
    cabin: Cabin

    @classmethod
    def from_raw(
        cls,
        pclass: Optional[str | int],
        fare: Optional[str | float],
        cabin: Optional[str],
    ) -> "ClassInfo":
        return cls(
            pclass=PClass.from_raw(str(pclass) if pclass is not None else None),
            fare=Fare.from_raw(fare),
            cabin=Cabin.from_raw(cabin),
        )

    @property
    def is_upper_class(self) -> bool:
        return self.pclass.value == PClassType.FIRST

    @property
    def is_upper_deck(self) -> bool:
        return self.cabin.is_upper_deck

    def __str__(self) -> str:
        return f"{self.pclass} / {self.fare} / {self.cabin}"
