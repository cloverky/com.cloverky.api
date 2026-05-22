import logging

from sqlalchemy.ext.asyncio import AsyncSession

from fridge.schemas.user_schema import FridgeUserCreate
from fridge.services.user_service import FridgeUserService
from models.user import User

logger = logging.getLogger(__name__)


class FridgeUserController:
    def __init__(self) -> None:
        self._service = FridgeUserService()

    async def get_profile(self, db: AsyncSession, user_id: int) -> User | None:
        return await self._service.get_profile(db, user_id)

    async def ensure_profile(self, db: AsyncSession, data: FridgeUserCreate) -> User:
        logger.info("[Fridge UserController] ensure_profile user_id=%s", data.user_id)
        return await self._service.ensure_profile(db, data)
