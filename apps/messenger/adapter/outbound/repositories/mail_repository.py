from __future__ import annotations

import logging

from messenger.app.dtos.mail_dto import MailMessengerQuery, MailMessengerResponse
from messenger.app.ports.output.mail_repository_port import MailRepositoryPort
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class MailPgRepository(MailRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(
        self, query: MailMessengerQuery
    ) -> MailMessengerResponse:
        logger.info("[MailPgRepository] introduce_myself 진입 | request_data=%s", query)
        return MailMessengerResponse(
            id=query.id,
            name=query.name,
            description=(
                "저는 메신저 서비스입니다. "
                "Exaone LLM이 내용을 다듬어 Gmail로 발송하며, "
                "n8n 웹훅 파이프라인을 통해 전달됩니다."
            ),
        )
