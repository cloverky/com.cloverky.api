from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from fridge.models.food import FridgeFood
from fridge.schemas.food_schema import FoodCreate


class FoodRepository:
    async def get_by_id(self, db: AsyncSession, food_id: int) -> FridgeFood | None:
        r = await db.execute(select(FridgeFood).where(FridgeFood.id == food_id).limit(1))
        return r.scalar_one_or_none()

    async def find_by_name(self, db: AsyncSession, name: str) -> FridgeFood | None:
        key = name.strip()
        r = await db.execute(
            select(FridgeFood).where(func.lower(FridgeFood.name) == key.lower()).limit(1),
        )
        return r.scalar_one_or_none()

    async def list_by_category(self, db: AsyncSession, category_id: int) -> list[FridgeFood]:
        r = await db.execute(
            select(FridgeFood)
            .where(FridgeFood.category_id == category_id)
            .order_by(FridgeFood.name),
        )
        return list(r.scalars().all())

    async def add(self, db: AsyncSession, data: FoodCreate) -> FridgeFood:
        row = FridgeFood(
            category_id=data.category_id,
            name=data.name.strip(),
            description=data.description.strip() if data.description else None,
            default_unit=data.default_unit.strip() or "개",
        )
        db.add(row)
        await db.flush()
        await db.refresh(row)
        return row

    async def create(self, db: AsyncSession, data: FoodCreate) -> FridgeFood:
        row = await self.add(db, data)
        await db.commit()
        return row
