"""
Entity — 동등성은 식별자(id)로 판단, VO를 조합해 도메인 규칙을 표현
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

from clover.apps.titanic.domain.value_objects.passenger_rose_model_vo import (
    PassengerClass,
    TicketNumber,
    Fare,
    Cabin,
    Embarkation,
)


@dataclass
class Booking:
    """
    Aggregate Root.
    승객 탑승 정보(예약/티켓 도메인).
    모든 상태 변경은 반드시 이 Entity의 메서드를 통해 이루어져야 한다.
    외부에서 VO를 직접 교체하는 행위는 허용하지 않는다.
    """

    # ── 식별자 ──────────────────────────────────
    _id: int                    # DB PK (인프라 관심사, 외부 노출 최소화)
    person_id: int              # persons 테이블 FK

    # ── 도메인 속성 (VO) ─────────────────────────
    passenger_class: PassengerClass
    ticket: Optional[TicketNumber]
    fare: Optional[Fare]
    cabin: Optional[Cabin]
    embarkation: Optional[Embarkation]

    # ── 도메인 이벤트 수집 버퍼 ─────────────────
    _domain_events: list = field(default_factory=list, init=False, repr=False)

    # ──────────────────────────────────────────
    # 식별자 접근
    # ──────────────────────────────────────────
    @property
    def id(self) -> int:
        return self._id

    # ──────────────────────────────────────────
    # 팩토리 메서드
    # ──────────────────────────────────────────
    @classmethod
    def create(
        cls,
        db_id: int,
        person_id: int,
        pclass: str | None,
        ticket: str | None,
        fare: str | float | None,
        cabin: str | None,
        embarked: str | None,
    ) -> Booking:
        """
        원시 값을 받아 VO 검증 후 Entity를 생성한다.
        유효하지 않은 값이면 ValueError를 발생시킨다.
        """
        return cls(
            _id=db_id,
            person_id=person_id,
            passenger_class=PassengerClass(pclass) if pclass is not None else PassengerClass("3"),
            ticket=TicketNumber(ticket) if ticket is not None else None,
            fare=Fare(float(fare)) if fare is not None else None,
            cabin=Cabin(cabin) if cabin is not None else None,
            embarkation=Embarkation(embarked) if embarked is not None else None,
        )

    # ──────────────────────────────────────────
    # 도메인 행위 (비즈니스 규칙)
    # ──────────────────────────────────────────
    def upgrade_class(self, new_class: str) -> None:
        """객실 등급 변경."""
        self.passenger_class = PassengerClass(new_class)

    def assign_cabin(self, new_cabin: str) -> None:
        """객실 번호 배정 또는 변경."""
        self.cabin = Cabin(new_cabin)

    def correct_fare(self, new_fare: float) -> None:
        """운임 정정 — VO 불변성을 지키며 교체."""
        self.fare = Fare(new_fare)

    # ──────────────────────────────────────────
    # 도메인 이벤트
    # ──────────────────────────────────────────
    def pull_domain_events(self) -> list:
        """이벤트를 꺼내고 버퍼를 비운다."""
        events, self._domain_events = self._domain_events, []
        return events

    # ──────────────────────────────────────────
    # 동등성: 식별자 기반
    # ──────────────────────────────────────────
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Booking):
            return NotImplemented
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)

    def __repr__(self) -> str:
        return (
            f"Booking(id={self._id}, person_id={self.person_id}, "
            f"class={self.passenger_class}, cabin={self.cabin})"
        )
