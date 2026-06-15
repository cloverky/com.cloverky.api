from __future__ import annotations

from abc import ABC, abstractmethod

from fridge.adapter.inbound.api.schemas.foods_schema import FoodCatalogSchema
from clover.apps.fridge.app.dtos.foods_dto import FoodCatalogResponse


class FoodsUseCase(ABC):

    @abstractmethod
    async def get_catalog(self, schema: FoodCatalogSchema) -> FoodCatalogResponse:
        pass
