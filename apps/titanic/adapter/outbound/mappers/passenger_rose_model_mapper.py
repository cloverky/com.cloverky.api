from __future__ import annotations
from typing import Optional

from clover.apps.titanic.adapter.outbound.orm.passenger_rose_model_orm import RoseModelOrm


class RoseModelMapper:
    """
    RoseModelOrm (bookings 테이블) ↔ 도메인 엔티티 매퍼.
    엔티티 정의가 완성되면 아래 TODO를 교체한다.
    columns: id, person_id (FK persons.id), pclass, ticket, fare, cabin, embarked
    """

    @staticmethod
    def to_entity(orm: RoseModelOrm):
        # TODO: 도메인 엔티티 정의 후 구현
        raise NotImplementedError("RoseModel 엔티티 정의 후 구현 필요")

    @staticmethod
    def to_orm(entity, existing: Optional[RoseModelOrm] = None) -> RoseModelOrm:
        # TODO: 도메인 엔티티 정의 후 구현
        raise NotImplementedError("RoseModel 엔티티 정의 후 구현 필요")
