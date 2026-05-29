import logging
from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.pg.walter_pg_repository import WalterPgRepository
from titanic.app.ports.input.walter_use_case import WalterUseCase
from titanic.app.ports.output.walter_repository import WalterRepository

logger = logging.getLogger(__name__)


class WalterQuery(WalterUseCase):
    """WalterUseCase 구현 — WalterRepository(조회 포트)만 의존한다."""

    def __init__(self, repository: WalterRepository | None = None):
        self._repository = repository or WalterPgRepository()

    async def list_passengers(
        self,
        db: AsyncSession,
        *,
        page: int,
        size: int,
    ) -> Dict[str, object]:
        logger.info("🎈 [WalterQuery] list_passengers 시작 — page=%d size=%d", page, size)
        result = await self._repository.list_passengers(db, page=page, size=size)
        logger.info(
            "🎈 [WalterQuery] list_passengers 완료 — returned=%d total=%s",
            len(result.get("items", [])),
            (result.get("pagination") or {}).get("totalCount"),
        )
        return result
