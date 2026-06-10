"""
Value Objects — 불변(immutable), 동등성은 값으로 판단, 자체 유효성 검증
"""
from __future__ import annotations
from dataclasses import dataclass


# ──────────────────────────────────────────────
# PassengerId VO
# ──────────────────────────────────────────────
@dataclass(frozen=True)
class PassengerId:
    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("PassengerId는 빈 값일 수 없습니다.")

    def __str__(self) -> str:
        return self.value


# ──────────────────────────────────────────────
# PassengerName VO
# ──────────────────────────────────────────────
@dataclass(frozen=True)
class PassengerName:
    value: str

    def __post_init__(self) -> None:
        stripped = self.value.strip() if self.value else ""
        if not stripped:
            raise ValueError("이름은 빈 값일 수 없습니다.")
        if len(stripped) > 100:
            raise ValueError("이름은 100자를 초과할 수 없습니다.")
        # frozen=True라 object.__setattr__ 우회
        object.__setattr__(self, "value", stripped)

    def __str__(self) -> str:
        return self.value


# ──────────────────────────────────────────────
# Gender VO
# ──────────────────────────────────────────────
@dataclass(frozen=True)
class Gender:
    MALE = "male"
    FEMALE = "female"

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower() if self.value else ""
        allowed = {self.MALE, self.FEMALE}
        if normalized not in allowed:
            raise ValueError(f"성별은 {allowed} 중 하나여야 합니다. 입력값: {self.value!r}")
        object.__setattr__(self, "value", normalized)

    @property
    def is_male(self) -> bool:
        return self.value == self.MALE

    @property
    def is_female(self) -> bool:
        return self.value == self.FEMALE

    def __str__(self) -> str:
        return self.value


# ──────────────────────────────────────────────
# Age VO
# ──────────────────────────────────────────────
@dataclass(frozen=True)
class Age:
    value: float

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("나이는 0 이상이어야 합니다.")
        if self.value > 150:
            raise ValueError("나이는 150을 초과할 수 없습니다.")

    @property
    def is_child(self) -> bool:
        return self.value < 18

    @property
    def is_adult(self) -> bool:
        return self.value >= 18

    def __str__(self) -> str:
        return str(self.value)


# ──────────────────────────────────────────────
# FamilyInfo VO  (SibSp + Parch를 하나의 VO로 묶음)
# 도메인 개념: 동반 가족 정보
# ──────────────────────────────────────────────
@dataclass(frozen=True)
class FamilyInfo:
    """
    sib_sp: 탑승한 형제/배우자 수
    parch : 탑승한 부모/자녀 수
    """
    sib_sp: int
    parch: int

    def __post_init__(self) -> None:
        if self.sib_sp < 0:
            raise ValueError("sib_sp는 0 이상이어야 합니다.")
        if self.parch < 0:
            raise ValueError("parch는 0 이상이어야 합니다.")

    @property
    def total_family_members(self) -> int:
        return self.sib_sp + self.parch

    @property
    def is_alone(self) -> bool:
        return self.total_family_members == 0


# ──────────────────────────────────────────────
# SurvivalStatus VO
# ──────────────────────────────────────────────
@dataclass(frozen=True)
class SurvivalStatus:
    SURVIVED = "survived"
    NOT_SURVIVED = "not_survived"
    UNKNOWN = "unknown"

    value: str

    def __post_init__(self) -> None:
        allowed = {self.SURVIVED, self.NOT_SURVIVED, self.UNKNOWN}
        if self.value not in allowed:
            raise ValueError(f"생존 상태는 {allowed} 중 하나여야 합니다.")

    @classmethod
    def from_raw(cls, raw: str | None) -> SurvivalStatus:
        """ORM의 raw 문자열 → VO 변환 팩토리"""
        if raw is None:
            return cls(cls.UNKNOWN)
        mapping = {
            "1": cls.SURVIVED,
            "true": cls.SURVIVED,
            "yes": cls.SURVIVED,
            "0": cls.NOT_SURVIVED,
            "false": cls.NOT_SURVIVED,
            "no": cls.NOT_SURVIVED,
        }
        normalized = raw.strip().lower()
        if normalized not in mapping:
            raise ValueError(f"생존 상태로 변환할 수 없는 값: {raw!r}")
        return cls(mapping[normalized])

    @property
    def is_survived(self) -> bool:
        return self.value == self.SURVIVED

    def __str__(self) -> str:
        return self.value