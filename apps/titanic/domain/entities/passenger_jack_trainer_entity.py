"""
Entity — 동등성은 식별자(id)로 판단, VO를 조합해 도메인 규칙을 표현
"""

from __future__ import annotations

from dataclasses import dataclass, field

from titanic.domain.value_objects.passenger_jack_trainer_vo import (
    Age,
    FamilyRelation,
    Gender,
    PassengerId,
    PassengerName,
    SurvivalStatus,
)


@dataclass
class PassengerEntity:
    id: int
    passenger_id: PassengerId | None
    name: PassengerName | None
    gender: Gender
    age: Age | None
    family_relation: FamilyRelation
    survival_status: SurvivalStatus
    _domain_events: list = field(default_factory=list, init=False, repr=False)

    # ── 팩토리 메서드 ─────────────────────────────
    @classmethod
    def create(
        cls,
        db_id: int,
        passenger_id: str,
        name: str,
        gender: str,
        age: float | None,
        sib_sp: int,
        parch: int,
        survived: str | None,
    ) -> PassengerEntity:
        return cls(
            id=db_id,
            passenger_id=PassengerId(passenger_id) if passenger_id else None,
            name=PassengerName(name) if name else None,
            gender=Gender.from_raw(gender),
            age=Age(age) if age is not None else None,
            family_relation=FamilyRelation(sib_sp=sib_sp, parch=parch),
            survival_status=SurvivalStatus.from_raw(survived),
        )

    @classmethod
    def from_orm(cls, orm) -> PassengerEntity:
        return cls(
            id=orm.id,
            passenger_id=PassengerId(orm.passenger_id) if orm.passenger_id else None,
            name=PassengerName(orm.name) if orm.name else None,
            gender=Gender.from_raw(orm.gender),
            age=Age.from_raw(str(orm.age) if orm.age is not None else None),
            family_relation=FamilyRelation.from_raw(orm.sib_sp, orm.parch),
            survival_status=SurvivalStatus.from_raw(orm.survived),
        )

    # ── 도메인 행위 ───────────────────────────────
    def is_high_risk(self) -> bool:
        """남성(또는 성별 미상) 성인 혼자 탑승 = 고위험군"""
        return (
            not self.gender.is_female()
            and self.age is not None
            and not self.age.is_unknown
            and self.age.is_adult
            and self.family_relation.is_alone
        )

    def has_family(self) -> bool:
        return not self.family_relation.is_alone

    def record_survival(self, survived: bool) -> None:
        self.survival_status = SurvivalStatus(survived=survived)

    def correct_age(self, new_age: float) -> None:
        self.age = Age(new_age)

    def correct_name(self, new_name: str) -> None:
        self.name = PassengerName(new_name)

    def pull_domain_events(self) -> list:
        events, self._domain_events = self._domain_events, []
        return events

    # ── 동등성: id 기반 ───────────────────────────
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PassengerEntity):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return (
            f"PassengerEntity(id={self.id}, passenger_id={self.passenger_id}, "
            f"name={self.name}, survival={self.survival_status})"
        )


# 하위 호환 alias
Passenger = PassengerEntity
