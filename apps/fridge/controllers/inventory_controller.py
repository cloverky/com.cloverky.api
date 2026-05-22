import logging

from sqlalchemy.ext.asyncio import AsyncSession

from fridge.models.inventory import FridgeInventory
from fridge.schemas.inventory_schema import InventoryCreate
from fridge.services.inventory_service import InventoryService

logger = logging.getLogger(__name__)


class InventoryController:
    def __init__(self) -> None:
        self._service = InventoryService()

    async def list_inventory(self, db: AsyncSession, user_id: int) -> list[FridgeInventory]:
        logger.debug("[Fridge InventoryController] list_inventory user_id=%s", user_id)
        return await self._service.list_inventory(db, user_id)

    async def get_line(self, db: AsyncSession, inventory_id: int) -> FridgeInventory | None:
        return await self._service.get_line(db, inventory_id)

    async def add_line(self, db: AsyncSession, data: InventoryCreate) -> FridgeInventory:
        logger.info(
            "[Fridge InventoryController] add_line user_id=%s food_id=%s",
            data.user_id,
            data.food_id,
        )
        return await self._service.add_line(db, data)
