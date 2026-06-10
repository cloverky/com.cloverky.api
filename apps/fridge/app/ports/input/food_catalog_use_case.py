from __future__ import annotations

from abc import ABC, abstractmethod

from fridge.app.dtos.food_catalog_dto import CreateFoodCommand, FoodDto


class FoodCatalogUseCase(ABC):

    @abstractmethod
    async def get_food(self, food_id: int) -> FoodDto | None:
        pass

    @abstractmethod
    async def list_foods(self, category_id: int) -> list[FoodDto]:
        pass

    @abstractmethod
    async def create_food(self, command: CreateFoodCommand) -> FoodDto:
        pass
