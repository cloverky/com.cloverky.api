from __future__ import annotations

from abc import ABC, abstractmethod

from fridge.app.dtos.inventory_dto import (
    AdjustInventoryCommand,
    CreateInventoryCommand,
    InventoryAdjustResultDto,
    InventoryExpiryResponse,
    InventoryItemDto,
    InventoryListDto,
    InventoryQuery,
)


class InventoryRepository(ABC):
    @abstractmethod
    async def get_urgent_items(self, query: InventoryQuery) -> InventoryExpiryResponse:
        pass

    @abstractmethod
    async def list_by_user_email(self, user_email: str) -> InventoryListDto:
        pass

    @abstractmethod
    async def create(self, cmd: CreateInventoryCommand) -> InventoryItemDto:
        pass

    @abstractmethod
    async def delete(self, user_email: str, item_id: int) -> None:
        pass

    @abstractmethod
    async def consume(self, cmd: AdjustInventoryCommand) -> InventoryAdjustResultDto:
        pass

    @abstractmethod
    async def add_quantity(
        self, cmd: AdjustInventoryCommand
    ) -> InventoryAdjustResultDto:
        pass
