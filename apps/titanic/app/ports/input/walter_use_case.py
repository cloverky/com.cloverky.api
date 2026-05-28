import logging
from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.pg.walter_pg_repository import WalterPgRepository
from titanic.app.ports.output.walter_repository import WalterRepository
from titanic.app.use_cases.walter_query import WalterQuery

logger = logging.getLogger(__name__)


class WalterUseCase:
    """승객 목록 조회용 인바운드 유스케이스."""

    def __init__(self, repository: WalterRepository | None = None):
        self.query = WalterQuery(repository or WalterPgRepository())

    async def execute(self, db: AsyncSession, *, page: int, size: int) -> Dict[str, object]:
        logger.info("[WalterUseCase] execute 시작 — page=%d size=%d", page, size)
        result = await self.query.execute(db, page=page, size=size)
        logger.info(
            "[WalterUseCase] execute 완료 — returned=%d total=%s",
            len(result.get("items", [])),
            (result.get("pagination") or {}).get("totalCount"),
        )
        return result
