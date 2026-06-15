from __future__ import annotations

from fridge.adapter.inbound.api.schemas.foods_schema import FoodCatalogSchema
from clover.apps.fridge.app.dtos.foods_dto import FoodsQuery, FoodCatalogResponse
from clover.apps.fridge.app.ports.input.foods_use_case import FoodsUseCase
from clover.apps.fridge.app.ports.output.foods_repository import FoodsRepository


class FoodsInteractor(FoodsUseCase):

    def __init__(self, repository: FoodsRepository) -> None:
        self.repository = repository

    async def get_catalog(self, schema: FoodCatalogSchema) -> FoodCatalogResponse:
        return await self.repository.get_catalog(FoodsQuery(
            category_id=schema.category_id,
            name=schema.name,
        ))
