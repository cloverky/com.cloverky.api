import logging

from sqlalchemy.ext.asyncio import AsyncSession

from fridge.models.category_model import FridgeCategory
from fridge.schemas.category_schema import CategoryCreate
from fridge.services.category_service import CategoryService

logger = logging.getLogger(__name__)


class CategoryController:
    def __init__(self) -> None:
        self._service = CategoryService()

    async def list_categories(self, db: AsyncSession) -> list[FridgeCategory]:
        logger.debug("[Fridge CategoryController] list_categories")
        return await self._service.list_categories(db)

    async def create_category(self, db: AsyncSession, data: CategoryCreate) -> FridgeCategory:
        logger.info("[Fridge CategoryController] create_category name=%r", data.name)
        return await self._service.create_category(db, data)
