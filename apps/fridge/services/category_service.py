from sqlalchemy.ext.asyncio import AsyncSession

from fridge.models.category import FridgeCategory
from fridge.repositories.category_repository import CategoryRepository
from fridge.schemas.category_schema import CategoryCreate


class CategoryService:
    def __init__(self) -> None:
        self._repo = CategoryRepository()

    async def list_categories(self, db: AsyncSession) -> list[FridgeCategory]:
        return await self._repo.list_all(db)

    async def create_category(self, db: AsyncSession, data: CategoryCreate) -> FridgeCategory:
        return await self._repo.create(db, data)
