from __future__ import annotations

from messenger.adapter.outbound.orm.discord_orm import DiscordOrm


class DiscordMapper:
    @staticmethod
    def to_entity(orm: DiscordOrm):
        raise NotImplementedError("Discord 엔티티 정의 후 구현 필요")

    @staticmethod
    def to_orm(entity, existing: DiscordOrm | None = None) -> DiscordOrm:
        raise NotImplementedError("Discord 엔티티 정의 후 구현 필요")
