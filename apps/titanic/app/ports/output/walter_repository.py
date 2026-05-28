import logging
from abc import ABC, abstractmethod
from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


def log_walter_repository_contract(page: int, size: int) -> None:
    logger.info("[WalterRepositoryPort] list_passengers 호출 예정 — page=%d size=%d", page, size)


class WalterRepository(ABC):
    """Walter 승객 목록 조회용 출력 포트."""

    @abstractmethod
    async def list_passengers(
        self,
        db: AsyncSession,
        *,
        page: int,
        size: int,
    ) -> Dict[str, object]:
        """승객 목록과 페이지 정보를 반환한다."""
