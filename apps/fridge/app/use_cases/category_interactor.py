from __future__ import annotations

from clover.apps.fridge.app.dtos.category_dto import CategoryQuery, CategoryResponse
from clover.apps.fridge.app.ports.input.category_use_case import CategoryUseCase
from clover.apps.fridge.app.ports.output.category_repository import CategoryRepository
from fridge.adapter.inbound.api.schemas.category_schema import CategorySchema


class CategoryInteractor(CategoryUseCase):
    def __init__(self, repository: CategoryRepository) -> None:
        self.repository = repository

    async def get_list(self, schema: CategorySchema) -> CategoryResponse:
        return await self.repository.get_list(
            CategoryQuery(
                name=schema.name,
            )
        )
