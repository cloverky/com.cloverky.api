import logging
from typing import Dict, List

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.ports.output.james_repository import (
    JamesRepository,
    log_repository_contract,
)

logger = logging.getLogger(__name__)


class JamesCommand:
    """james_use_case에서 전달된 row 데이터를 repository로 넘기는 커맨드."""

    def __init__(self, repository: JamesRepository):
        self._repository = repository

    async def execute(
        self,
        db: AsyncSession,
        rows: List[Dict[str, str]],
    ) -> Dict[str, object]:
        logger.info("[JamesCommand] repository 전달 시작 — rows=%d", len(rows))
        log_repository_contract(len(rows))
        result = await self._repository.save_rows(db, rows)
        logger.info(
            "[JamesCommand] repository 전달 완료 — saved=%s",
            result.get("count"),
        )
        return result
