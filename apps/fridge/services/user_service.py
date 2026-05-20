from sqlalchemy.ext.asyncio import AsyncSession

from fridge.models.user import FridgeUser
from fridge.repositories.user_repository import FridgeUserRepository
from fridge.schemas.user_schema import FridgeUserCreate


class FridgeUserService:
    def __init__(self) -> None:
        self._repo = FridgeUserRepository()

    async def get_profile(self, db: AsyncSession, user_id: int) -> FridgeUser | None:
        return await self._repo.get_by_user_id(db, user_id)

    async def ensure_profile(self, db: AsyncSession, data: FridgeUserCreate) -> FridgeUser:
        existing = await self._repo.get_by_user_id(db, data.user_id)
        if existing:
            return existing
        return await self._repo.create(db, data)
