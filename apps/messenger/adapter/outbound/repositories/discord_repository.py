from __future__ import annotations

import logging
import os

import httpx
from messenger.app.dtos.discord_dto import (
    DiscordMessengerQuery,
    DiscordMessengerResponse,
    DiscordSendCommand,
    DiscordSendResult,
)
from messenger.app.ports.output.discord_repository_port import DiscordRepositoryPort
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")


class DiscordPgRepository(DiscordRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def send(self, cmd: DiscordSendCommand) -> DiscordSendResult:
        logger.info("[DiscordPgRepository] send 진입 | username=%r", cmd.username)
        if not _WEBHOOK_URL:
            return DiscordSendResult(
                success=False,
                message="DISCORD_WEBHOOK_URL 환경변수가 설정되지 않았습니다.",
            )
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                _WEBHOOK_URL,
                json={"content": cmd.content, "username": cmd.username},
                timeout=10,
            )
        if resp.status_code in (200, 204):
            return DiscordSendResult(success=True, message="디스코드 메시지 전송 완료")
        return DiscordSendResult(
            success=False,
            message=f"전송 실패 (status={resp.status_code})",
        )

    async def introduce_myself(
        self, query: DiscordMessengerQuery
    ) -> DiscordMessengerResponse:
        logger.info(
            "[DiscordPgRepository] introduce_myself 진입 | request_data=%s", query
        )
        return DiscordMessengerResponse(
            id=query.id,
            name=query.name,
            description=(
                "저는 디스코드 메신저 서비스입니다. "
                "Discord 웹훅을 통해 채널에 메시지를 전송합니다. "
                "DISCORD_WEBHOOK_URL 환경변수로 웹훅 URL을 설정하세요."
            ),
        )
