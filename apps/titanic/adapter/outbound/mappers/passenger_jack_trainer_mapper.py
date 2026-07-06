from __future__ import annotations

from titanic.adapter.outbound.orm.passenger_jack_trainer_orm import JackTrainerOrm
from titanic.domain.entities.passenger_jack_trainer_entity import PassengerEntity
from titanic.domain.value_objects.passenger_jack_trainer_vo import (
    Age,
    FamilyRelation,
    Gender,
    PassengerId,
    PassengerName,
    SurvivalStatus,
)


class JackTrainerMapper:
    @staticmethod
    def to_entity(orm: JackTrainerOrm) -> PassengerEntity:
        return PassengerEntity(
            id=orm.id,
            passenger_id=PassengerId(orm.passenger_id) if orm.passenger_id else None,
            name=PassengerName(orm.name) if orm.name else None,
            gender=Gender.from_raw(orm.gender),
            age=Age(float(orm.age)) if orm.age is not None else None,
            family_relation=FamilyRelation(
                sib_sp=int(orm.sib_sp) if orm.sib_sp is not None else 0,
                parch=int(orm.parch) if orm.parch is not None else 0,
            ),
            survival_status=SurvivalStatus.from_raw(orm.survived),
        )

    @staticmethod
    def to_orm(
        entity: PassengerEntity, existing: JackTrainerOrm | None = None
    ) -> JackTrainerOrm:
        # BUG: JackTrainerOrm has no 'id' column — raises TypeError (tracked as Red, fix pending)
        orm = existing or JackTrainerOrm(id=entity.id)
        orm.passenger_id = entity.passenger_id.value if entity.passenger_id else None
        orm.name = entity.name.value if entity.name else None
        orm.gender = str(entity.gender)
        orm.age = (
            str(entity.age.value) if entity.age and not entity.age.is_unknown else None
        )
        orm.sib_sp = str(entity.family_relation.sib_sp)
        orm.parch = str(entity.family_relation.parch)
        orm.survived = str(entity.survival_status.survived)
        return orm
