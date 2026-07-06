from __future__ import annotations

from abc import ABC, abstractmethod

from clover.apps.fridge.app.dtos.user_dto import UserResponse
from fridge.adapter.inbound.api.schemas.user_schema import UserSchema


class UserUseCase(ABC):
    @abstractmethod
    async def get_me(self, schema: UserSchema) -> UserResponse:
        pass
