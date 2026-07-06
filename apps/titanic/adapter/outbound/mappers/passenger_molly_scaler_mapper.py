from __future__ import annotations

from clover.apps.titanic.adapter.outbound.orm.passenger_molly_scaler_orm import (
    MollyScalerOrm,
)


class MollyScalerMapper:
    @staticmethod
    def to_entity(orm: MollyScalerOrm):
        # TODO: 도메인 엔티티 및 ORM 테이블 정의 후 구현
        raise NotImplementedError("MollyScaler 엔티티 정의 후 구현 필요")

    @staticmethod
    def to_orm(entity, existing: MollyScalerOrm | None = None) -> MollyScalerOrm:
        # TODO: 도메인 엔티티 및 ORM 테이블 정의 후 구현
        raise NotImplementedError("MollyScaler 엔티티 정의 후 구현 필요")
