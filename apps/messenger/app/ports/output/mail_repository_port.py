from __future__ import annotations

from abc import ABC, abstractmethod

from messenger.app.dtos.mail_dto import MailMessengerQuery, MailMessengerResponse


class MailRepositoryPort(ABC):
    @abstractmethod
    async def introduce_myself(
        self, query: MailMessengerQuery
    ) -> MailMessengerResponse:
        """메신저 서비스 자기소개 레포지토리 추상 메서드"""
