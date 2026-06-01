from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession


class JamesDirectorRepository(ABC):

    @abstractmethod
    async def receive_uploaded_records(
        self,
        db: AsyncSession,
        records: list[dict[str, Any]],
    ) -> dict[str, Any]:
        ...
