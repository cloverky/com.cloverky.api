"""
Value Objects — 불변(immutable), 동등성은 값으로 판단, 자체 유효성 검증
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class GenderType(str, Enum):
    MALE = "male"
    FEMALE = "female"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class PassengerId:
    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("PassengerId는 빈 값일 수 없습니다.")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class PassengerName:
    value: str

    def __post_init__(self) -> None:
        stripped = self.value.strip() if self.value else ""
        if not stripped:
            raise ValueError("이름은 빈 값일 수 없습니다.")
        if len(stripped) > 200:
            raise ValueError("이름은 200자를 초과할 수 없습니다.")
        object.__setattr__(self, "value", stripped)

    @property
    def full_name(self) -> str:
        return self.value

    @property
    def normalized(self) -> str:
        return self.value

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class Gender:
    value: GenderType

    @classmethod
    def from_raw(cls, raw: str | None) -> Gender:
        if raw is None:
            return cls(value=GenderType.UNKNOWN)
        normalized = raw.strip().lower()
        if normalized == "male":
            return cls(value=GenderType.MALE)
        if normalized == "female":
            return cls(value=GenderType.FEMALE)
        return cls(value=GenderType.UNKNOWN)

    def is_female(self) -> bool:
        return self.value == GenderType.FEMALE

    def is_male(self) -> bool:
        return self.value == GenderType.MALE

    def __str__(self) -> str:
        return self.value.value


@dataclass(frozen=True)
class Age:
    value: float | None

    def __post_init__(self) -> None:
        if self.value is None:
            return
        if self.value < 0:
            raise ValueError("나이는 0 이상이어야 합니다.")
        if self.value > 120:
            raise ValueError("나이는 120을 초과할 수 없습니다.")

    @classmethod
    def from_raw(cls, raw: str | None) -> Age:
        if raw is None or (isinstance(raw, str) and raw.strip() == ""):
            return cls(value=None)
        try:
            return cls(value=float(str(raw).strip()))
        except (ValueError, AttributeError):
            raise ValueError(f"파싱 실패: {raw!r}")

    @property
    def is_unknown(self) -> bool:
        return self.value is None

    @property
    def is_minor(self) -> bool:
        if self.value is None:
            return False
        return self.value < 18

    @property
    def is_adult(self) -> bool:
        if self.value is None:
            return False
        return self.value >= 18

    def __str__(self) -> str:
        return str(self.value) if self.value is not None else "unknown"


@dataclass(frozen=True)
class FamilyRelation:
    sib_sp: int
    parch: int

    def __post_init__(self) -> None:
        if self.sib_sp < 0:
            raise ValueError("sib_sp는 0 이상이어야 합니다.")
        if self.parch < 0:
            raise ValueError("parch는 0 이상이어야 합니다.")

    @classmethod
    def from_raw(cls, sib_sp: str | None, parch: str | None) -> FamilyRelation:
        return cls(
            sib_sp=int(sib_sp) if sib_sp else 0,
            parch=int(parch) if parch else 0,
        )

    @property
    def total_family_size(self) -> int:
        return self.sib_sp + self.parch

    @property
    def is_alone(self) -> bool:
        return self.total_family_size == 0


FamilyInfo = FamilyRelation


@dataclass(frozen=True)
class SurvivalStatus:
    survived: bool | None = None

    @classmethod
    def from_raw(cls, raw: str | None) -> SurvivalStatus:
        if raw is None or (isinstance(raw, str) and raw.strip() == ""):
            return cls(survived=None)
        mapping: dict[str, bool] = {
            "1": True, "true": True, "yes": True,
            "0": False, "false": False, "no": False,
        }
        normalized = raw.strip().lower()
        if normalized not in mapping:
            raise ValueError(f"파싱 실패: {raw!r}")
        return cls(survived=mapping[normalized])

    @property
    def is_unknown(self) -> bool:
        return self.survived is None

    @property
    def is_survived(self) -> bool:
        return self.survived is True
