from sqlalchemy.ext.asyncio import AsyncSession

from fridge.models.food_model import FridgeFood
from fridge.repositories.food_repository import FoodRepository
from fridge.schemas.food_schema import FoodCreate


class FoodService:
    def __init__(self) -> None:
        self._repo = FoodRepository()

    async def get_food(self, db: AsyncSession, food_id: int) -> FridgeFood | None:
        return await self._repo.get_by_id(db, food_id)

    async def list_foods(self, db: AsyncSession, category_id: int) -> list[FridgeFood]:
        return await self._repo.list_by_category(db, category_id)

    async def create_food(self, db: AsyncSession, data: FoodCreate) -> FridgeFood:
        return await self._repo.create(db, data)
