from abc import ABC, abstractmethod


class MailGateway(ABC):
    @abstractmethod
    async def send(self, to: str, subject: str, body: str) -> None: ...
