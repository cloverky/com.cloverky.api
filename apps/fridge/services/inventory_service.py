from sqlalchemy.ext.asyncio import AsyncSession

from fridge.models.inventory_model import FridgeInventory
from fridge.repositories.inventory_repository import InventoryRepository
from fridge.schemas.inventory_schema import InventoryCreate


class InventoryService:
    def __init__(self) -> None:
        self._repo = InventoryRepository()

    async def list_inventory(self, db: AsyncSession, user_id: int) -> list[FridgeInventory]:
        return await self._repo.list_by_user(db, user_id)

    async def get_line(self, db: AsyncSession, inventory_id: int) -> FridgeInventory | None:
        return await self._repo.get_by_id(db, inventory_id)

    async def add_line(self, db: AsyncSession, data: InventoryCreate) -> FridgeInventory:
        return await self._repo.create(db, data)
