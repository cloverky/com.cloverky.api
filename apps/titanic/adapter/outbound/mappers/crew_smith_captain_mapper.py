from __future__ import annotations

from clover.apps.titanic.adapter.outbound.orm.crew_smith_captain_orm import (
    SmithCaptainOrm,
)


class SmithCaptainMapper:
    @staticmethod
    def to_entity(orm: SmithCaptainOrm):
        # TODO: 도메인 엔티티 및 ORM 테이블 정의 후 구현
        raise NotImplementedError("SmithCaptain 엔티티 정의 후 구현 필요")

    @staticmethod
    def to_orm(entity, existing: SmithCaptainOrm | None = None) -> SmithCaptainOrm:
        # TODO: 도메인 엔티티 및 ORM 테이블 정의 후 구현
        raise NotImplementedError("SmithCaptain 엔티티 정의 후 구현 필요")
