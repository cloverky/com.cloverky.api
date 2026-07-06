from __future__ import annotations

from abc import ABC, abstractmethod

from fridge.adapter.inbound.api.schemas.inventory_schema import InventoryExpirySchema
from fridge.app.dtos.inventory_dto import (
    AdjustInventoryCommand,
    CreateInventoryCommand,
    ExpiryEstimateDto,
    InventoryAdjustResultDto,
    InventoryExpiryResponse,
    InventoryItemDto,
    InventoryListDto,
)


class InventoryUseCase(ABC):
    @abstractmethod
    async def get_urgent_items(
        self, schema: InventoryExpirySchema
    ) -> InventoryExpiryResponse:
        pass

    @abstractmethod
    async def list_inventory(self, user_email: str) -> InventoryListDto:
        pass

    @abstractmethod
    async def create_item(self, cmd: CreateInventoryCommand) -> InventoryItemDto:
        pass

    @abstractmethod
    async def delete_item(self, user_email: str, item_id: int) -> None:
        pass

    @abstractmethod
    async def consume_item(
        self, cmd: AdjustInventoryCommand
    ) -> InventoryAdjustResultDto:
        pass

    @abstractmethod
    async def add_quantity(
        self, cmd: AdjustInventoryCommand
    ) -> InventoryAdjustResultDto:
        pass

    @abstractmethod
    async def estimate_expiry(
        self, name: str, purchased_date: str, storage: str
    ) -> ExpiryEstimateDto:
        pass
