from __future__ import annotations
from typing import Optional

from clover.apps.titanic.adapter.outbound.orm.crew_hartley_violin_orm import HartleyViolinOrm


class HartleyViolinMapper:

    @staticmethod
    def to_entity(orm: HartleyViolinOrm):
        # TODO: 도메인 엔티티 및 ORM 테이블 정의 후 구현
        raise NotImplementedError("HartleyViolin 엔티티 정의 후 구현 필요")

    @staticmethod
    def to_orm(entity, existing: Optional[HartleyViolinOrm] = None) -> HartleyViolinOrm:
        # TODO: 도메인 엔티티 및 ORM 테이블 정의 후 구현
        raise NotImplementedError("HartleyViolin 엔티티 정의 후 구현 필요")
