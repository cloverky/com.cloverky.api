from __future__ import annotations

from clover.apps.titanic.adapter.outbound.orm.passenger_isidor_couple_orm import (
    IsidorCoupleOrm,
)


class IsidorCoupleMapper:
    @staticmethod
    def to_entity(orm: IsidorCoupleOrm):
        # TODO: 도메인 엔티티 및 ORM 테이블 정의 후 구현
        raise NotImplementedError("IsidorCouple 엔티티 정의 후 구현 필요")

    @staticmethod
    def to_orm(entity, existing: IsidorCoupleOrm | None = None) -> IsidorCoupleOrm:
        # TODO: 도메인 엔티티 및 ORM 테이블 정의 후 구현
        raise NotImplementedError("IsidorCouple 엔티티 정의 후 구현 필요")
