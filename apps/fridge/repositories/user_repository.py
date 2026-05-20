from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fridge.models.user import FridgeUser
from fridge.schemas.user_schema import FridgeUserCreate


class FridgeUserRepository:
    async def get_by_user_id(self, db: AsyncSession, user_id: int) -> FridgeUser | None:
        r = await db.execute(select(FridgeUser).where(FridgeUser.user_id == user_id).limit(1))
        return r.scalar_one_or_none()

    async def create(self, db: AsyncSession, data: FridgeUserCreate) -> FridgeUser:
        row = FridgeUser(
            user_id=data.user_id,
            default_storage=data.default_storage.strip() or "냉장",
        )
        db.add(row)
        await db.commit()
        await db.refresh(row)
        return row
