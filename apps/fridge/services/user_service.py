from sqlalchemy.ext.asyncio import AsyncSession

from fridge.repositories.user_repository import FridgeUserRepository
from fridge.schemas.user_schema import FridgeUserCreate
from models.user import User


class FridgeUserService:
    def __init__(self) -> None:
        self._repo = FridgeUserRepository()

    async def get_profile(self, db: AsyncSession, user_id: int) -> User | None:
        return await self._repo.get_by_user_id(db, user_id)

    async def ensure_profile(self, db: AsyncSession, data: FridgeUserCreate) -> User:
        return await self._repo.ensure_default_storage(db, data)
