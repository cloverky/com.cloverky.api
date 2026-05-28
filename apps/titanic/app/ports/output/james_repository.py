import logging
from abc import ABC, abstractmethod
from typing import Dict, List

from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


def log_repository_contract(row_count: int) -> None:
    """출력 포트로 전달되는 데이터 개수를 로깅한다."""
    logger.info("[JamesRepositoryPort] save_rows 호출 예정 — rows=%d", row_count)


class JamesRepository(ABC):
    """James CSV 업로드 row 저장용 출력 포트."""

    @abstractmethod
    async def save_rows(
        self,
        db: AsyncSession,
        rows: List[Dict[str, str]],
    ) -> Dict[str, object]:
        """james_command에서 전달된 row 목록을 Neon DB에 저장하고 결과를 반환한다."""
