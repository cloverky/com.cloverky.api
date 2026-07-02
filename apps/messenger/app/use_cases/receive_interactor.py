from __future__ import annotations

import asyncio
import logging
import os

from messenger.app.ports.input.receive_use_case import ReceiveUseCase
from messenger.app.ports.output.receive_port import ReceiveRepositoryPort

logger = logging.getLogger(__name__)


class ReceiveInteractor(ReceiveUseCase):
    def __init__(self, repository: ReceiveRepositoryPort) -> None:
        self._repository = repository

    async def embed_and_store(self, mail_id: int, text: str) -> None:
        try:
            embedding = await asyncio.to_thread(self._generate_embedding, text)
            await self._repository.update_embedding(mail_id, embedding)
            logger.info("임베딩 저장 완료 — mail_id: %d, dim: %d", mail_id, len(embedding))
        except Exception:
            logger.exception("임베딩 생성/저장 실패 — mail_id: %d", mail_id)

    @staticmethod
    def _generate_embedding(text: str) -> list[float]:
        import ollama

        client = ollama.Client(host=os.getenv("OLLAMA_HOST", "http://localhost:11434"))
        result = client.embed(
            model="nomic-embed-text",
            input=f"search_document: {text}",
        )
        return result.embeddings[0]
