from abc import ABC, abstractmethod


class ReceiveRepositoryPort(ABC):
    @abstractmethod
    async def update_embedding(self, mail_id: int, embedding: list[float]) -> None: ...
