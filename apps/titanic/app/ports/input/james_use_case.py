import logging
from typing import Dict, List

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.pg.james_pg_repository import JamesPgRepository
from titanic.app.ports.output.james_repository import JamesRepository
from titanic.app.use_cases.james_command import JamesCommand

logger = logging.getLogger(__name__)


class JamesUseCase:
    """Inbound router가 전달한 Titanic row 데이터를 받는 유스케이스."""

    def __init__(self, repository: JamesRepository | None = None):
        self.command = JamesCommand(repository or JamesPgRepository())

    async def execute(
        self,
        db: AsyncSession,
        rows: List[Dict[str, str]],
    ) -> Dict[str, object]:
        logger.info("[JamesUseCase] execute 시작 — rows=%d", len(rows))
        result = await self.command.execute(db, rows)
        logger.info(
            "[JamesUseCase] execute 완료 — saved=%s",
            result.get("count"),
        )
        return result
