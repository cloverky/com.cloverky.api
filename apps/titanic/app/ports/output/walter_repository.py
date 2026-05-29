from abc import ABC, abstractmethod
from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession


class WalterRepository(ABC):
    """승객 목록 조회 전용 아웃바운드 포트 (ISP: read만 노출)."""

    @abstractmethod
    async def list_passengers(
        self,
        db: AsyncSession,
        *,
        page: int,
        size: int,
    ) -> Dict[str, object]:
        """승객 목록과 페이지 정보를 반환한다."""
