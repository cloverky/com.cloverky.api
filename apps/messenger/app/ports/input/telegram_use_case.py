from __future__ import annotations

from abc import ABC, abstractmethod

from messenger.app.dtos.telegram_dto import (
    TelegramMessengerQuery,
    TelegramMessengerResponse,
    TelegramSendCommand,
    TelegramSendResult,
)


class TelegramUseCase(ABC):
    @abstractmethod
    async def send(self, cmd: TelegramSendCommand) -> TelegramSendResult:
        """텔레그램 채팅방에 메시지를 전송한다"""

    @abstractmethod
    async def introduce_myself(
        self, query: TelegramMessengerQuery
    ) -> TelegramMessengerResponse:
        """텔레그램 메신저 서비스 자기소개"""
