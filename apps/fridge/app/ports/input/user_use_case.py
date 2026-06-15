from __future__ import annotations

from abc import ABC, abstractmethod

from fridge.adapter.inbound.api.schemas.user_schema import UserSchema
from clover.apps.fridge.app.dtos.user_dto import UserResponse


class UserUseCase(ABC):

    @abstractmethod
    async def get_me(self, schema: UserSchema) -> UserResponse:
        pass
