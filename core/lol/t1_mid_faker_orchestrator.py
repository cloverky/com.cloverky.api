"""Faker Orchestrator — exaone3.5:2.4b 로컬 모델 오케스트레이터."""

from __future__ import annotations

import os
from collections.abc import Generator
from functools import lru_cache

import ollama

_MODEL = "exaone3.5:2.4b"
_DEFAULT_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")


class FakerOrchestrator:
    def __init__(self, host: str = _DEFAULT_HOST) -> None:
        self._client = ollama.Client(host=host)
        self._async_client = ollama.AsyncClient(host=host)

    def is_ready(self) -> bool:
        try:
            models = self._client.list()
            return any(m.model == _MODEL for m in models.models)
        except Exception:
            return False

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        stream: bool = False,
    ) -> str | Generator[str, None, None]:
        if stream:
            return self._stream(messages)
        response = self._client.chat(model=_MODEL, messages=messages)
        return response.message.content or ""

    def _stream(self, messages: list[dict[str, str]]) -> Generator[str, None, None]:
        for chunk in self._client.chat(model=_MODEL, messages=messages, stream=True):
            content = chunk.message.content
            if content:
                yield content

    async def achat(self, messages: list[dict[str, str]]) -> str:
        response = await self._async_client.chat(model=_MODEL, messages=messages)
        return response.message.content or ""

    async def achat_stream(
        self, messages: list[dict[str, str]]
    ) -> Generator[str, None, None]:
        async for chunk in await self._async_client.chat(
            model=_MODEL, messages=messages, stream=True
        ):
            content = chunk.message.content
            if content:
                yield content


@lru_cache(maxsize=1)
def get_faker_orchestrator() -> FakerOrchestrator:
    return FakerOrchestrator()
