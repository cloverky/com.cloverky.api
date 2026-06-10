from __future__ import annotations
from typing import Optional

from clover.apps.titanic.adapter.outbound.orm.passenger_jack_trainer_orm import JackTrainerOrm
from clover.apps.titanic.domain.entities.passenger_jack_trainer_entity import Passenger
from clover.apps.titanic.domain.value_objects.passenger_jack_trainer_vo import (
    PassengerId,
    PassengerName,
    Gender,
    Age,
    FamilyInfo,
    SurvivalStatus,
)


class PassengerJackTrainerMapper:

    @staticmethod
    def to_entity(orm: JackTrainerOrm) -> Passenger:
        return Passenger.create(
            db_id=orm.id,
            passenger_id=orm.passenger_id or "",
            name=orm.name or "",
            gender=orm.gender or "",
            age=float(orm.age) if orm.age is not None else None,
            sib_sp=int(orm.sib_sp) if orm.sib_sp is not None else 0,
            parch=int(orm.parch) if orm.parch is not None else 0,
            survived=orm.survived,
        )

    @staticmethod
    def to_orm(entity: Passenger, existing: Optional[JackTrainerOrm] = None) -> JackTrainerOrm:
        orm = existing or JackTrainerOrm()
        orm.passenger_id = entity.passenger_id.value
        orm.name = entity.name.value
        orm.gender = entity.gender.value
        orm.age = str(entity.age.value) if entity.age else None
        orm.sib_sp = str(entity.family_info.sib_sp)
        orm.parch = str(entity.family_info.parch)
        orm.survived = entity.survival_status.value
        return orm
