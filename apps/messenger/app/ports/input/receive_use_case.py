from abc import ABC, abstractmethod


class ReceiveUseCase(ABC):
    @abstractmethod
    async def embed_and_store(self, mail_id: int, text: str) -> None: ...
