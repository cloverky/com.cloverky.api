from __future__ import annotations

from datetime import date, timedelta

from fridge.adapter.inbound.api.schemas.inventory_schema import InventoryExpirySchema
from fridge.app.dtos.inventory_dto import (
    AdjustInventoryCommand,
    CreateInventoryCommand,
    ExpiryEstimateDto,
    InventoryAdjustResultDto,
    InventoryExpiryResponse,
    InventoryItemDto,
    InventoryListDto,
    InventoryQuery,
)
from fridge.app.ports.input.inventory_use_case import InventoryUseCase
from fridge.app.ports.output.inventory_repository import InventoryRepository

_SHELF_LIFE: dict[str, dict[str, int]] = {
    "우유": {"냉장": 7, "냉동": 30, "실온": 1},
    "계란": {"냉장": 21, "냉동": 60, "실온": 7},
    "두부": {"냉장": 5, "냉동": 30, "실온": 1},
    "돼지고기": {"냉장": 3, "냉동": 90, "실온": 0},
    "소고기": {"냉장": 3, "냉동": 90, "실온": 0},
    "닭고기": {"냉장": 2, "냉동": 60, "실온": 0},
    "양파": {"냉장": 30, "냉동": 90, "실온": 30},
    "당근": {"냉장": 14, "냉동": 60, "실온": 7},
    "감자": {"냉장": 30, "냉동": 90, "실온": 14},
    "대파": {"냉장": 7, "냉동": 30, "실온": 2},
    "시금치": {"냉장": 5, "냉동": 30, "실온": 1},
    "배추": {"냉장": 14, "냉동": 60, "실온": 3},
    "상추": {"냉장": 5, "냉동": 14, "실온": 1},
    "토마토": {"냉장": 7, "냉동": 30, "실온": 3},
    "오이": {"냉장": 7, "냉동": 30, "실온": 2},
    "버섯": {"냉장": 5, "냉동": 30, "실온": 1},
}
_DEFAULT = {"냉장": 7, "냉동": 30, "실온": 3}


def _shelf_days(name: str, storage: str) -> int:
    for key, val in _SHELF_LIFE.items():
        if key in name:
            return val.get(storage, _DEFAULT.get(storage, 7))
    return _DEFAULT.get(storage, 7)


class InventoryInteractor(InventoryUseCase):
    def __init__(self, repository: InventoryRepository) -> None:
        self.repository = repository

    async def get_urgent_items(
        self, schema: InventoryExpirySchema
    ) -> InventoryExpiryResponse:
        return await self.repository.get_urgent_items(
            InventoryQuery(
                user_id=schema.user_id,
                food_id=schema.food_id,
            )
        )

    async def list_inventory(self, user_email: str) -> InventoryListDto:
        return await self.repository.list_by_user_email(user_email)

    async def create_item(self, cmd: CreateInventoryCommand) -> InventoryItemDto:
        return await self.repository.create(cmd)

    async def delete_item(self, user_email: str, item_id: int) -> None:
        await self.repository.delete(user_email, item_id)

    async def consume_item(
        self, cmd: AdjustInventoryCommand
    ) -> InventoryAdjustResultDto:
        return await self.repository.consume(cmd)

    async def add_quantity(
        self, cmd: AdjustInventoryCommand
    ) -> InventoryAdjustResultDto:
        return await self.repository.add_quantity(cmd)

    async def estimate_expiry(
        self, name: str, purchased_date: str, storage: str
    ) -> ExpiryEstimateDto:
        days = _shelf_days(name, storage)
        purchased = date.fromisoformat(purchased_date)
        estimated = purchased + timedelta(days=days)
        return ExpiryEstimateDto(
            name=name,
            purchased_date=purchased_date,
            storage=storage,
            shelf_life_days=days,
            estimated_expiry_date=str(estimated),
            message=f"{name}의 {storage} 보관 기준 유통기한은 약 {days}일입니다.",
        )
