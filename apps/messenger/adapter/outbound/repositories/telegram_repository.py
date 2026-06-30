from __future__ import annotations

import logging
import os

import httpx
from messenger.app.dtos.telegram_dto import (
    TelegramMessengerQuery,
    TelegramMessengerResponse,
    TelegramSendCommand,
    TelegramSendResult,
)
from messenger.app.ports.output.telegram_repository_port import TelegramRepositoryPort
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

_N8N_WEBHOOK_URL = os.getenv("N8N_TELEGRAM_WEBHOOK_URL", "")
_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
_MY_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
_API_BASE = "https://api.telegram.org/bot"


class TelegramPgRepository(TelegramRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def send(self, cmd: TelegramSendCommand) -> TelegramSendResult:
        logger.info("[TelegramPgRepository] send 진입 | chat_id=%r", cmd.chat_id)
        if _N8N_WEBHOOK_URL:
            return await self._send_via_n8n(cmd)
        return await self._send_direct(cmd)

    async def _send_via_n8n(self, cmd: TelegramSendCommand) -> TelegramSendResult:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(
                _N8N_WEBHOOK_URL,
                json={"chat_id": cmd.chat_id, "text": cmd.text},
            )
        if resp.is_success:
            return TelegramSendResult(
                success=True, message="텔레그램 메시지 전송 완료 (n8n)"
            )
        return TelegramSendResult(
            success=False,
            message=f"n8n 전송 실패: {resp.status_code}",
        )

    async def _send_direct(self, cmd: TelegramSendCommand) -> TelegramSendResult:
        if not _BOT_TOKEN:
            return TelegramSendResult(
                success=False,
                message="TELEGRAM_BOT_TOKEN 환경변수가 설정되지 않았습니다.",
            )
        url = f"{_API_BASE}{_BOT_TOKEN}/sendMessage"
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                url,
                json={"chat_id": cmd.chat_id, "text": cmd.text},
            )
        data = resp.json()
        if data.get("ok"):
            return TelegramSendResult(success=True, message="텔레그램 메시지 전송 완료")
        return TelegramSendResult(
            success=False,
            message=f"전송 실패: {data.get('description', '알 수 없는 오류')}",
        )

    async def introduce_myself(
        self, query: TelegramMessengerQuery
    ) -> TelegramMessengerResponse:
        return TelegramMessengerResponse(
            id=query.id,
            name=query.name,
            description=(
                "저는 텔레그램 메신저 서비스입니다. "
                "n8n 워크플로우를 통해 Telegram Bot API로 메시지를 전송합니다."
            ),
        )
