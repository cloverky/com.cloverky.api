from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from clover.apps.fridge.app.dtos.inventory_dto import InventoryQuery, InventoryExpiryResponse
from clover.apps.fridge.app.ports.output.inventory_repository import InventoryRepository

logger = logging.getLogger(__name__)


class InventoryPgRepository(InventoryRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_urgent_items(self, query: InventoryQuery) -> InventoryExpiryResponse:
        logger.info(f"[InventoryPgRepository] get_urgent_items | query={query}")
        return InventoryExpiryResponse(
            id=1,
            food_id=query.food_id,
        )
