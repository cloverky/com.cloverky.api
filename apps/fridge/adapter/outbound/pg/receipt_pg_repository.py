from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from clover.apps.fridge.app.dtos.receipt_dto import ReceiptQuery, ReceiptUploadResponse
from clover.apps.fridge.app.ports.output.receipt_repository import ReceiptRepository

logger = logging.getLogger(__name__)


class ReceiptPgRepository(ReceiptRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_status(self, query: ReceiptQuery) -> ReceiptUploadResponse:
        logger.info(f"[ReceiptPgRepository] get_status | query={query}")
        return ReceiptUploadResponse(
            id=1,
            status=query.status,
        )
