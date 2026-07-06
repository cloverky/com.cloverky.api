from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from clover.apps.fridge.app.dtos.receipt_line_dto import (
    ReceiptLineQuery,
    ReceiptLineResponse,
)
from clover.apps.fridge.app.ports.output.receipt_line_repository import (
    ReceiptLineRepository,
)

logger = logging.getLogger(__name__)


class ReceiptLinePgRepository(ReceiptLineRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_lines(self, query: ReceiptLineQuery) -> ReceiptLineResponse:
        logger.info(f"[ReceiptLinePgRepository] get_lines | query={query}")
        return ReceiptLineResponse(
            id=1,
            line_name="사과",
        )
