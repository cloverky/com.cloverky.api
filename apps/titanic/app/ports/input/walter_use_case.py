from abc import ABC, abstractmethod
from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession


class WalterUseCase(ABC):
    """승객 목록 조회 전용 인바운드 포트 (ISP: 읽기 작업만 노출)."""

    @abstractmethod
    async def list_passengers(
        self,
        db: AsyncSession,
        *,
        page: int,
        size: int,
    ) -> Dict[str, object]:
        """페이지 단위 승객 목록을 반환한다."""
