from __future__ import annotations

from abc import ABC, abstractmethod

from clover.apps.fridge.app.dtos.foods_dto import FoodCatalogResponse
from fridge.adapter.inbound.api.schemas.foods_schema import FoodCatalogSchema


class FoodsUseCase(ABC):
    @abstractmethod
    async def get_catalog(self, schema: FoodCatalogSchema) -> FoodCatalogResponse:
        pass
