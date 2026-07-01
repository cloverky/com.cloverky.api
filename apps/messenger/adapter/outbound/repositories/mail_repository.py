from __future__ import annotations

import logging

from messenger.adapter.outbound.orm.mail_orm import MailInboxOrm
from messenger.app.dtos.mail_dto import (
    MailInboxItem,
    MailInboxReceiveCommand,
    MailMessengerQuery,
    MailMessengerResponse,
)
from messenger.app.ports.output.mail_repository_port import MailRepositoryPort
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class MailPgRepository(MailRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(
        self, query: MailMessengerQuery
    ) -> MailMessengerResponse:
        return MailMessengerResponse(
            id=query.id,
            name=query.name,
            description=(
                "저는 메신저 서비스입니다. "
                "Exaone LLM이 내용을 다듬어 Gmail로 발송하며, "
                "n8n 웹훅 파이프라인을 통해 전달됩니다."
            ),
        )

    async def save_inbox(self, cmd: MailInboxReceiveCommand) -> MailInboxItem:
        row = MailInboxOrm(
            from_email=cmd.from_email,
            subject=cmd.subject,
            body=cmd.body,
        )
        self.session.add(row)
        await self.session.commit()
        await self.session.refresh(row)
        return MailInboxItem(
            id=row.id,
            from_email=row.from_email,
            subject=row.subject,
            body=row.body,
            received_at=row.received_at,
        )

    async def list_inbox(self, limit: int = 50) -> list[MailInboxItem]:
        result = await self.session.execute(
            select(MailInboxOrm)
            .order_by(MailInboxOrm.received_at.desc())
            .limit(limit)
        )
        rows = result.scalars().all()
        return [
            MailInboxItem(
                id=r.id,
                from_email=r.from_email,
                subject=r.subject,
                body=r.body,
                received_at=r.received_at,
            )
            for r in rows
        ]
