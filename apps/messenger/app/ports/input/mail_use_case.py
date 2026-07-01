from abc import ABC, abstractmethod

from messenger.app.dtos.mail_dto import (
    MailCommand,
    MailInboxItem,
    MailInboxListResult,
    MailInboxReceiveCommand,
    MailMessengerQuery,
    MailMessengerResponse,
    MailResult,
)


class MailUseCase(ABC):
    @abstractmethod
    async def send_mail(self, cmd: MailCommand) -> MailResult: ...

    @abstractmethod
    async def receive_mail(self, cmd: MailInboxReceiveCommand) -> MailInboxItem: ...

    @abstractmethod
    async def list_inbox(self, limit: int = 50) -> MailInboxListResult: ...

    @abstractmethod
    async def introduce_myself(
        self, query: MailMessengerQuery
    ) -> MailMessengerResponse: ...
