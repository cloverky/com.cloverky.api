from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date

from fridge.app.dtos.inventory_dto import (
    AdjustInventoryResultDto,
    CreateInventoryCommand,
    ExpiryEstimateDto,
    InventoryItemDto,
    InventoryListDto,
    UpdateInventoryCommand,
)


class InventoryUseCase(ABC):

    @abstractmethod
    async def estimate_expiry(self, name: str, purchased_date: date, storage: str) -> ExpiryEstimateDto:
        pass

    @abstractmethod
    async def list_inventory(self, user_email: str) -> InventoryListDto:
        pass

    @abstractmethod
    async def create_item(self, user_email: str, command: CreateInventoryCommand) -> InventoryItemDto:
        pass

    @abstractmethod
    async def update_item(
        self,
        user_email: str,
        item_id: int,
        command: UpdateInventoryCommand,
    ) -> InventoryItemDto:
        pass

    @abstractmethod
    async def consume_item(self, user_email: str, item_id: int, amount: int) -> AdjustInventoryResultDto:
        pass

    @abstractmethod
    async def add_quantity(self, user_email: str, item_id: int, amount: int) -> AdjustInventoryResultDto:
        pass

    @abstractmethod
    async def delete_item(self, user_email: str, item_id: int) -> None:
        pass
