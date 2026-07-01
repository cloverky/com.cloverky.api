from __future__ import annotations

from abc import ABC, abstractmethod

from messenger.app.dtos.mail_dto import (
    MailInboxItem,
    MailInboxReceiveCommand,
    MailMessengerQuery,
    MailMessengerResponse,
)


class MailRepositoryPort(ABC):
    @abstractmethod
    async def introduce_myself(
        self, query: MailMessengerQuery
    ) -> MailMessengerResponse: ...

    @abstractmethod
    async def save_inbox(self, cmd: MailInboxReceiveCommand) -> MailInboxItem: ...

    @abstractmethod
    async def list_inbox(self, limit: int = 50) -> list[MailInboxItem]: ...
