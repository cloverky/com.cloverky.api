from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fridge.models.inventory import FridgeInventory
from fridge.schemas.inventory_schema import InventoryCreate


class InventoryRepository:
    async def list_by_user(self, db: AsyncSession, user_id: int) -> list[FridgeInventory]:
        r = await db.execute(
            select(FridgeInventory)
            .where(FridgeInventory.user_id == user_id)
            .order_by(FridgeInventory.id.desc()),
        )
        return list(r.scalars().all())

    async def get_by_id(self, db: AsyncSession, inventory_id: int) -> FridgeInventory | None:
        r = await db.execute(select(FridgeInventory).where(FridgeInventory.id == inventory_id).limit(1))
        return r.scalar_one_or_none()

    async def add(self, db: AsyncSession, data: InventoryCreate) -> FridgeInventory:
        row = FridgeInventory(
            user_id=data.user_id,
            food_id=data.food_id,
            quantity=data.quantity,
            unit=data.unit.strip() or "개",
            expiry_date=data.expiry_date,
            purchased_date=data.purchased_date,
            expiry_is_estimated=data.expiry_is_estimated,
            storage=data.storage.strip() or "냉장",
        )
        db.add(row)
        await db.flush()
        await db.refresh(row)
        return row

    async def create(self, db: AsyncSession, data: InventoryCreate) -> FridgeInventory:
        row = await self.add(db, data)
        await db.commit()
        return row
