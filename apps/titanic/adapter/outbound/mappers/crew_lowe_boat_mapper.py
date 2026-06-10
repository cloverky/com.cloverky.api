from __future__ import annotations
from typing import Optional

from clover.apps.titanic.adapter.outbound.orm.crew_lowe_boat_orm import LoweBoatOrm


class LoweBoatMapper:

    @staticmethod
    def to_entity(orm: LoweBoatOrm):
        # TODO: 도메인 엔티티 및 ORM 테이블 정의 후 구현
        raise NotImplementedError("LoweBeat 엔티티 정의 후 구현 필요")

    @staticmethod
    def to_orm(entity, existing: Optional[LoweBoatOrm] = None) -> LoweBoatOrm:
        # TODO: 도메인 엔티티 및 ORM 테이블 정의 후 구현
        raise NotImplementedError("LoweBoat 엔티티 정의 후 구현 필요")
