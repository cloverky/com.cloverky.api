from __future__ import annotations

from abc import ABC, abstractmethod

from fridge.app.dtos.food_catalog_dto import CategoryDto, CreateCategoryCommand


class CategoryRepository(ABC):

    @abstractmethod
    async def get_or_create_default(self, name: str, sort_order: int = 999) -> int:
        pass

    @abstractmethod
    async def list_all(self) -> list[CategoryDto]:
        pass

    @abstractmethod
    async def create_category(self, command: CreateCategoryCommand) -> CategoryDto:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass
