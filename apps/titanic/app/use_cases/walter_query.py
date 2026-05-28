import logging
from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.ports.output.walter_repository import (
    WalterRepository,
    log_walter_repository_contract,
)

logger = logging.getLogger(__name__)


class WalterQuery:
    """승객 목록 조회를 repository로 위임하는 쿼리 유스케이스."""

    def __init__(self, repository: WalterRepository):
        self._repository = repository

    async def execute(self, db: AsyncSession, *, page: int, size: int) -> Dict[str, object]:
        logger.info("[WalterQuery] repository 조회 시작 — page=%d size=%d", page, size)
        log_walter_repository_contract(page, size)
        result = await self._repository.list_passengers(db, page=page, size=size)
        logger.info(
            "[WalterQuery] repository 조회 완료 — returned=%d",
            len(result.get("items", [])),
        )
        return result
