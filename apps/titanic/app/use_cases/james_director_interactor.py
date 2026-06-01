from __future__ import annotations

import logging
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.ports.input.james_director_use_case import JamesDirectorUseCase
from titanic.app.ports.output.james_director_repository import JamesDirectorRepository

logger = logging.getLogger(__name__)


class JamesDirectorInteractor(JamesDirectorUseCase):
    """JamesUseCase 구현 — JamesRepository(저장 포트)만 의존한다."""

    def __init__(self, repository: JamesDirectorRepository, *, db: AsyncSession) -> None:
        self._repository = repository
        self._db = db

    async def receive_uploaded_records(self, records: list[dict[str, Any]]) -> dict[str, Any]:
        logger.info("🍀 [JamesCommand] receive_uploaded_records 시작 — records=%d", len(records))
        return await self._repository.receive_uploaded_records(self._db, records)


JamesCommand = JamesDirectorInteractor
