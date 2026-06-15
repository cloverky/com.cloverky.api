from __future__ import annotations

from fridge.adapter.inbound.api.schemas.inventory_schema import InventoryExpirySchema
from clover.apps.fridge.app.dtos.inventory_dto import InventoryQuery, InventoryExpiryResponse
from clover.apps.fridge.app.ports.input.inventory_use_case import InventoryUseCase
from clover.apps.fridge.app.ports.output.inventory_repository import InventoryRepository


class InventoryInteractor(InventoryUseCase):

    def __init__(self, repository: InventoryRepository) -> None:
        self.repository = repository

    async def get_urgent_items(self, schema: InventoryExpirySchema) -> InventoryExpiryResponse:
        return await self.repository.get_urgent_items(InventoryQuery(
            user_id=schema.user_id,
            food_id=schema.food_id,
        ))
