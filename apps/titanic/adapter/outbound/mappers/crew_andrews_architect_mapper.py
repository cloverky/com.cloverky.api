from __future__ import annotations

from clover.apps.titanic.adapter.outbound.orm.crew_andrews_architect_orm import (
    CrewAndrewsArchitectOrm,
)


class AndrewsArchitectMapper:
    @staticmethod
    def to_entity(orm: CrewAndrewsArchitectOrm):
        # TODO: 도메인 엔티티 및 ORM 테이블 정의 후 구현
        raise NotImplementedError("AndrewsArchitect 엔티티 정의 후 구현 필요")

    @staticmethod
    def to_orm(
        entity, existing: CrewAndrewsArchitectOrm | None = None
    ) -> CrewAndrewsArchitectOrm:
        # TODO: 도메인 엔티티 및 ORM 테이블 정의 후 구현
        raise NotImplementedError("AndrewsArchitect 엔티티 정의 후 구현 필요")
