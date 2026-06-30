from __future__ import annotations

from abc import ABC, abstractmethod

from messenger.app.dtos.discord_dto import (
    DiscordMessengerQuery,
    DiscordMessengerResponse,
    DiscordSendCommand,
    DiscordSendResult,
)


class DiscordUseCase(ABC):
    @abstractmethod
    async def send(self, cmd: DiscordSendCommand) -> DiscordSendResult:
        """디스코드 채널에 메시지를 전송한다"""

    @abstractmethod
    async def introduce_myself(
        self, query: DiscordMessengerQuery
    ) -> DiscordMessengerResponse:
        """디스코드 메신저 서비스 자기소개"""
