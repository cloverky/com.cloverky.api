from __future__ import annotations

from typing import Optional

from clover.apps.silicon_valley.adapter.outbound.orm.piper_hendricks_ceo_orm import HendricksCeoOrm


class HendricksCeoMapper:

    @staticmethod
    def to_entity(orm: HendricksCeoOrm):
        # TODO: 도메인 엔티티 및 ORM 테이블 정의 후 구현
        raise NotImplementedError("HendricksCeo 엔티티 정의 후 구현 필요")

    @staticmethod
    def to_orm(entity, existing: Optional[HendricksCeoOrm] = None) -> HendricksCeoOrm:
        # TODO: 도메인 엔티티 및 ORM 테이블 정의 후 구현
        raise NotImplementedError("HendricksCeo 엔티티 정의 후 구현 필요")
