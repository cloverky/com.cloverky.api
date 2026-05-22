from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fridge.schemas.user_schema import FridgeUserCreate
from models.user import User


class FridgeUserRepository:
    async def get_by_user_id(self, db: AsyncSession, user_id: int) -> User | None:
        r = await db.execute(select(User).where(User.id == user_id).limit(1))
        return r.scalar_one_or_none()

    async def ensure_default_storage(
        self,
        db: AsyncSession,
        data: FridgeUserCreate,
    ) -> User:
        user = await self.get_by_user_id(db, data.user_id)
        if user is None:
            raise ValueError(f"users.id={data.user_id} 가 없습니다.")
        user.default_storage = data.default_storage.strip() or "냉장"
        await db.commit()
        await db.refresh(user)
        return user
