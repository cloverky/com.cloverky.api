from __future__ import annotations

from abc import ABC, abstractmethod

from clover.apps.fridge.app.dtos.foods_dto import FoodsQuery, FoodCatalogResponse


class FoodsRepository(ABC):

    @abstractmethod
    async def get_catalog(self, query: FoodsQuery) -> FoodCatalogResponse:
        pass
