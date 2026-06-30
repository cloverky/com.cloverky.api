from __future__ import annotations

import logging

from messenger.app.dtos.discord_dto import (
    DiscordMessengerQuery,
    DiscordMessengerResponse,
    DiscordSendCommand,
    DiscordSendResult,
)
from messenger.app.ports.input.discord_use_case import DiscordUseCase
from messenger.app.ports.output.discord_repository_port import DiscordRepositoryPort

logger = logging.getLogger(__name__)


class DiscordInteractor(DiscordUseCase):
    def __init__(self, repository: DiscordRepositoryPort) -> None:
        self._repository = repository

    async def send(self, cmd: DiscordSendCommand) -> DiscordSendResult:
        logger.info("[DiscordInteractor] 메시지 전송 | username=%r", cmd.username)
        return await self._repository.send(cmd)

    async def introduce_myself(
        self, query: DiscordMessengerQuery
    ) -> DiscordMessengerResponse:
        return await self._repository.introduce_myself(query)
