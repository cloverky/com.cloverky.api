from __future__ import annotations

from abc import ABC, abstractmethod

from clover.apps.fridge.app.dtos.inventory_dto import InventoryQuery, InventoryExpiryResponse


class InventoryRepository(ABC):

    @abstractmethod
    async def get_urgent_items(self, query: InventoryQuery) -> InventoryExpiryResponse:
        pass
