from __future__ import annotations

from abc import ABC, abstractmethod

from clover.apps.fridge.app.dtos.category_dto import CategoryQuery, CategoryResponse


class CategoryRepository(ABC):

    @abstractmethod
    async def get_list(self, query: CategoryQuery) -> CategoryResponse:
        pass
