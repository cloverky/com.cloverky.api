from __future__ import annotations

from clover.apps.titanic.adapter.outbound.orm.crew_walter_roaster_orm import (
    WalterRoasterOrm,
)


class WalterRoasterMapper:
    @staticmethod
    def to_entity(orm: WalterRoasterOrm):
        # TODO: 도메인 엔티티 및 ORM 테이블 정의 후 구현
        raise NotImplementedError("WalterRoaster 엔티티 정의 후 구현 필요")

    @staticmethod
    def to_orm(entity, existing: WalterRoasterOrm | None = None) -> WalterRoasterOrm:
        # TODO: 도메인 엔티티 및 ORM 테이블 정의 후 구현
        raise NotImplementedError("WalterRoaster 엔티티 정의 후 구현 필요")
