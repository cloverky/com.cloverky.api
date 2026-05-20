from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fridge.models.category_model import FridgeCategory
from fridge.schemas.category_schema import CategoryCreate


class CategoryRepository:
    async def list_all(self, db: AsyncSession) -> list[FridgeCategory]:
        r = await db.execute(select(FridgeCategory).order_by(FridgeCategory.sort_order, FridgeCategory.id))
        return list(r.scalars().all())

    async def get_by_id(self, db: AsyncSession, category_id: int) -> FridgeCategory | None:
        r = await db.execute(select(FridgeCategory).where(FridgeCategory.id == category_id).limit(1))
        return r.scalar_one_or_none()

    async def create(self, db: AsyncSession, data: CategoryCreate) -> FridgeCategory:
        row = FridgeCategory(name=data.name.strip(), sort_order=data.sort_order)
        db.add(row)
        await db.commit()
        await db.refresh(row)
        return row
