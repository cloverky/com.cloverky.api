import logging

from sqlalchemy.ext.asyncio import AsyncSession

from fridge.models.food_model import FridgeFood
from fridge.schemas.food_schema import FoodCreate
from fridge.services.food_service import FoodService

logger = logging.getLogger(__name__)


class FoodController:
    def __init__(self) -> None:
        self._service = FoodService()

    async def get_food(self, db: AsyncSession, food_id: int) -> FridgeFood | None:
        return await self._service.get_food(db, food_id)

    async def list_foods(self, db: AsyncSession, category_id: int) -> list[FridgeFood]:
        logger.debug("[Fridge FoodController] list_foods category_id=%s", category_id)
        return await self._service.list_foods(db, category_id)

    async def create_food(self, db: AsyncSession, data: FoodCreate) -> FridgeFood:
        logger.info("[Fridge FoodController] create_food name=%r", data.name)
        return await self._service.create_food(db, data)
