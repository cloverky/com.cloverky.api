from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession


class JamesRepository(ABC):

    @abstractmethod
    async def save_rows(self, db: AsyncSession, rows: list[dict[str, Any]]) -> dict[str, Any]:
        ...
