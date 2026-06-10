"""
Value Objects — 불변(immutable), 동등성은 값으로 판단, 자체 유효성 검증
"""
from __future__ import annotations
from dataclasses import dataclass


# ──────────────────────────────────────────────
# PassengerClass VO
# ──────────────────────────────────────────────
@dataclass(frozen=True)
class PassengerClass:
    FIRST = "1"
    SECOND = "2"
    THIRD = "3"

    value: str

    def __post_init__(self) -> None:
        normalized = str(self.value).strip()
        allowed = {self.FIRST, self.SECOND, self.THIRD}
        if normalized not in allowed:
            raise ValueError(f"객실 등급은 {allowed} 중 하나여야 합니다. 입력값: {self.value!r}")
        object.__setattr__(self, "value", normalized)

    @property
    def is_first_class(self) -> bool:
        return self.value == self.FIRST

    def __str__(self) -> str:
        return self.value


# ──────────────────────────────────────────────
# TicketNumber VO
# ──────────────────────────────────────────────
@dataclass(frozen=True)
class TicketNumber:
    value: str

    def __post_init__(self) -> None:
        stripped = self.value.strip() if self.value else ""
        if not stripped:
            raise ValueError("티켓 번호는 빈 값일 수 없습니다.")
        object.__setattr__(self, "value", stripped)

    def __str__(self) -> str:
        return self.value


# ──────────────────────────────────────────────
# Fare VO
# ──────────────────────────────────────────────
@dataclass(frozen=True)
class Fare:
    value: float

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("운임은 0 이상이어야 합니다.")

    @property
    def is_free(self) -> bool:
        return self.value == 0.0

    def __str__(self) -> str:
        return str(self.value)


# ──────────────────────────────────────────────
# Cabin VO
# ──────────────────────────────────────────────
@dataclass(frozen=True)
class Cabin:
    value: str

    def __post_init__(self) -> None:
        stripped = self.value.strip() if self.value else ""
        if not stripped:
            raise ValueError("객실 번호는 빈 값일 수 없습니다.")
        object.__setattr__(self, "value", stripped)

    @property
    def deck(self) -> str:
        return self.value[0].upper()

    def __str__(self) -> str:
        return self.value


# ──────────────────────────────────────────────
# Embarkation VO
# ──────────────────────────────────────────────
@dataclass(frozen=True)
class Embarkation:
    SOUTHAMPTON = "S"
    CHERBOURG = "C"
    QUEENSTOWN = "Q"

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().upper() if self.value else ""
        allowed = {self.SOUTHAMPTON, self.CHERBOURG, self.QUEENSTOWN}
        if normalized not in allowed:
            raise ValueError(f"탑승항은 {allowed} 중 하나여야 합니다. 입력값: {self.value!r}")
        object.__setattr__(self, "value", normalized)

    @property
    def port_name(self) -> str:
        names = {
            self.SOUTHAMPTON: "Southampton",
            self.CHERBOURG: "Cherbourg",
            self.QUEENSTOWN: "Queenstown",
        }
        return names[self.value]

    def __str__(self) -> str:
        return self.value
