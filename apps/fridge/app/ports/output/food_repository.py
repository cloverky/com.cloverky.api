from __future__ import annotations

from abc import ABC, abstractmethod

from fridge.app.dtos.food_catalog_dto import CreateFoodCommand, FoodDto


class FoodRepository(ABC):

    @abstractmethod
    async def find_by_name(self, name: str) -> int | None:
        pass

    @abstractmethod
    async def create(self, category_id: int, name: str, default_unit: str) -> int:
        pass

    @abstractmethod
    async def get_by_id(self, food_id: int) -> FoodDto | None:
        pass

    @abstractmethod
    async def list_by_category(self, category_id: int) -> list[FoodDto]:
        pass

    @abstractmethod
    async def create_food(self, command: CreateFoodCommand) -> FoodDto:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass
