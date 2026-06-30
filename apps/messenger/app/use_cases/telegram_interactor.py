from __future__ import annotations

import logging

from messenger.app.dtos.telegram_dto import (
    TelegramMessengerQuery,
    TelegramMessengerResponse,
    TelegramSendCommand,
    TelegramSendResult,
)
from messenger.app.ports.input.telegram_use_case import TelegramUseCase
from messenger.app.ports.output.telegram_repository_port import TelegramRepositoryPort

logger = logging.getLogger(__name__)


class TelegramInteractor(TelegramUseCase):
    def __init__(self, repository: TelegramRepositoryPort) -> None:
        self._repository = repository

    async def send(self, cmd: TelegramSendCommand) -> TelegramSendResult:
        logger.info("[TelegramInteractor] 메시지 전송 | chat_id=%r", cmd.chat_id)
        return await self._repository.send(cmd)

    async def introduce_myself(
        self, query: TelegramMessengerQuery
    ) -> TelegramMessengerResponse:
        return await self._repository.introduce_myself(query)
