from __future__ import annotations

from abc import ABC, abstractmethod

from clover.apps.fridge.app.dtos.user_dto import UserQuery, UserResponse


class UserRepository(ABC):
    @abstractmethod
    async def get_me(self, query: UserQuery) -> UserResponse:
        pass
