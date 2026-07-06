from __future__ import annotations

from abc import ABC, abstractmethod

from clover.apps.fridge.app.dtos.category_dto import CategoryResponse
from fridge.adapter.inbound.api.schemas.category_schema import CategorySchema


class CategoryUseCase(ABC):
    @abstractmethod
    async def get_list(self, schema: CategorySchema) -> CategoryResponse:
        pass
