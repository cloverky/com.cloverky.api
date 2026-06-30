from __future__ import annotations

from abc import ABC, abstractmethod

from messenger.app.dtos.telegram_dto import (
    TelegramMessengerQuery,
    TelegramMessengerResponse,
    TelegramSendCommand,
    TelegramSendResult,
)


class TelegramRepositoryPort(ABC):
    @abstractmethod
    async def send(self, cmd: TelegramSendCommand) -> TelegramSendResult:
        """텔레그램 Bot API로 메시지를 전송한다"""

    @abstractmethod
    async def introduce_myself(
        self, query: TelegramMessengerQuery
    ) -> TelegramMessengerResponse:
        """텔레그램 메신저 서비스 자기소개 레포지토리 추상 메서드"""
