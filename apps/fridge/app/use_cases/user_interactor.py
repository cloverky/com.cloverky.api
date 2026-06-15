from __future__ import annotations

from fridge.adapter.inbound.api.schemas.user_schema import UserSchema
from clover.apps.fridge.app.dtos.user_dto import UserQuery, UserResponse
from clover.apps.fridge.app.ports.input.user_use_case import UserUseCase
from clover.apps.fridge.app.ports.output.user_repository import UserRepository


class UserInteractor(UserUseCase):

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def get_me(self, schema: UserSchema) -> UserResponse:
        return await self.repository.get_me(UserQuery(
            username=schema.username,
        ))
