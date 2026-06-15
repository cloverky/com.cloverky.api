from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from clover.apps.fridge.app.dtos.user_dto import UserQuery, UserResponse
from clover.apps.fridge.app.ports.output.user_repository import UserRepository

logger = logging.getLogger(__name__)


class UserPgRepository(UserRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_me(self, query: UserQuery) -> UserResponse:
        logger.info(f"[UserPgRepository] get_me | query={query}")
        return UserResponse(
            id=1,
            username=query.username,
        )
