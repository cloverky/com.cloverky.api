from abc import ABC, abstractmethod

from messenger.app.dtos.mail_dto import (
    MailCommand,
    MailMessengerQuery,
    MailMessengerResponse,
    MailResult,
)


class MailUseCase(ABC):
    @abstractmethod
    async def send_mail(self, cmd: MailCommand) -> MailResult: ...

    @abstractmethod
    async def introduce_myself(
        self, query: MailMessengerQuery
    ) -> MailMessengerResponse:
        """메신저 서비스 자기소개"""
