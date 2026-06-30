from __future__ import annotations

from messenger.adapter.outbound.orm.mail_orm import MailOrm


class MailMapper:
    @staticmethod
    def to_entity(orm: MailOrm):
        raise NotImplementedError("Mail 엔티티 정의 후 구현 필요")

    @staticmethod
    def to_orm(entity, existing: MailOrm | None = None) -> MailOrm:
        raise NotImplementedError("Mail 엔티티 정의 후 구현 필요")
