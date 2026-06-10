from __future__ import annotations

from abc import ABC, abstractmethod

from fridge.app.dtos.food_catalog_dto import CategoryDto, CreateCategoryCommand


class CategoryCatalogUseCase(ABC):

    @abstractmethod
    async def list_categories(self) -> list[CategoryDto]:
        pass

    @abstractmethod
    async def create_category(self, command: CreateCategoryCommand) -> CategoryDto:
        pass
