from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession


class WalterRepository(ABC):

    @abstractmethod
    async def list_passengers(
        self,
        db: AsyncSession,
        *,
        page: int,
        size: int,
    ) -> dict[str, Any]:
        ...
