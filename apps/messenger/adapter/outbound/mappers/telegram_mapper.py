from __future__ import annotations

from messenger.adapter.outbound.orm.telegram_orm import TelegramOrm


class TelegramMapper:
    @staticmethod
    def to_entity(orm: TelegramOrm):
        raise NotImplementedError("Telegram 엔티티 정의 후 구현 필요")

    @staticmethod
    def to_orm(entity, existing: TelegramOrm | None = None) -> TelegramOrm:
        raise NotImplementedError("Telegram 엔티티 정의 후 구현 필요")
