from __future__ import annotations

from abc import ABC, abstractmethod

from messenger.app.dtos.discord_dto import (
    DiscordMessengerQuery,
    DiscordMessengerResponse,
    DiscordSendCommand,
    DiscordSendResult,
)


class DiscordRepositoryPort(ABC):
    @abstractmethod
    async def send(self, cmd: DiscordSendCommand) -> DiscordSendResult:
        """디스코드 웹훅 또는 Bot API로 메시지를 전송한다"""

    @abstractmethod
    async def introduce_myself(
        self, query: DiscordMessengerQuery
    ) -> DiscordMessengerResponse:
        """디스코드 메신저 서비스 자기소개 레포지토리 추상 메서드"""
