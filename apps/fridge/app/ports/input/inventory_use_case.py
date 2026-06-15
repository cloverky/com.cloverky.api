from __future__ import annotations

from abc import ABC, abstractmethod

from fridge.adapter.inbound.api.schemas.inventory_schema import InventoryExpirySchema
from clover.apps.fridge.app.dtos.inventory_dto import InventoryExpiryResponse


class InventoryUseCase(ABC):

    @abstractmethod
    async def get_urgent_items(self, schema: InventoryExpirySchema) -> InventoryExpiryResponse:
        pass
