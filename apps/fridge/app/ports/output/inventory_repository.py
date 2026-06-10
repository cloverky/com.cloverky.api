from __future__ import annotations

from abc import ABC, abstractmethod

from fridge.app.dtos.inventory_dto import CreateInventoryCommand, InventoryItemDto, UpdateInventoryCommand


class InventoryRepository(ABC):

    @abstractmethod
    async def list_by_user(self, user_id: int) -> list[InventoryItemDto]:
        pass

    @abstractmethod
    async def get_owned(self, user_id: int, item_id: int) -> InventoryItemDto:
        pass

    @abstractmethod
    async def create(self, command: CreateInventoryCommand, food_id: int) -> InventoryItemDto:
        pass

    @abstractmethod
    async def update(
        self,
        user_id: int,
        item_id: int,
        command: UpdateInventoryCommand,
        food_id: int | None = None,
    ) -> InventoryItemDto:
        pass

    @abstractmethod
    async def adjust_quantity(
        self,
        user_id: int,
        item_id: int,
        delta: int,
    ) -> tuple[InventoryItemDto | None, bool]:
        """delta 음수=소비. 반환: (item or None if removed, removed flag)."""
        pass

    @abstractmethod
    async def delete(self, user_id: int, item_id: int) -> None:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass
