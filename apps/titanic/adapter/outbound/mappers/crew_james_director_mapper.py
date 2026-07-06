from __future__ import annotations

from clover.apps.titanic.adapter.outbound.orm.crew_james_director_orm import (
    JamesDirectorOrm,
)


class JamesDirectorMapper:
    @staticmethod
    def to_entity(orm: JamesDirectorOrm):
        # TODO: 도메인 엔티티 및 ORM 테이블 정의 후 구현
        raise NotImplementedError("JamesDirector 엔티티 정의 후 구현 필요")

    @staticmethod
    def to_orm(entity, existing: JamesDirectorOrm | None = None) -> JamesDirectorOrm:
        # TODO: 도메인 엔티티 및 ORM 테이블 정의 후 구현
        raise NotImplementedError("JamesDirector 엔티티 정의 후 구현 필요")
