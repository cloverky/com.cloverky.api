from __future__ import annotations

from messenger.adapter.outbound.orm.juso_orm import JusoOrm


class JusoMapper:
    @staticmethod
    def to_entity(orm: JusoOrm):
        raise NotImplementedError("Juso 엔티티 정의 후 구현 필요")

    @staticmethod
    def to_orm(entity, existing: JusoOrm | None = None) -> JusoOrm:
        raise NotImplementedError("Juso 엔티티 정의 후 구현 필요")
