from __future__ import annotations

from typing import Optional

from clover.apps.silicon_valley.adapter.outbound.orm.piper_dunn_coo_orm import DunnCooOrm


class DunnCooMapper:

    @staticmethod
    def to_entity(orm: DunnCooOrm):
        # TODO: 도메인 엔티티 및 ORM 테이블 정의 후 구현
        raise NotImplementedError("DunnCoo 엔티티 정의 후 구현 필요")

    @staticmethod
    def to_orm(entity, existing: Optional[DunnCooOrm] = None) -> DunnCooOrm:
        # TODO: 도메인 엔티티 및 ORM 테이블 정의 후 구현
        raise NotImplementedError("DunnCoo 엔티티 정의 후 구현 필요")
