from __future__ import annotations

from datetime import date

from fastapi import HTTPException

from fridge.app.use_cases._shelf_life import (
    DEFAULT_MIN_QUANTITY,
    InventoryStatusItem,
    STORAGE_CHOICES,
    UNIT_CHOICES,
    compute_status,
    count_expiring_soon,
    count_low_stock,
    estimate_shelf_life_days,
    expiry_from_purchase,
    format_quantity,
    shelf_life_hint,
)
from fridge.app.dtos.inventory_dto import (
    AdjustInventoryResultDto,
    CreateInventoryCommand,
    ExpiryEstimateDto,
    InventoryItemDto,
    InventoryListDto,
    InventoryStatsDto,
    UpdateInventoryCommand,
)
from fridge.app.ports.input.inventory_use_case import InventoryUseCase
from fridge.app.ports.output.category_repository import CategoryRepository
from fridge.app.ports.output.food_repository import FoodRepository
from fridge.app.ports.output.inventory_repository import InventoryRepository
from fridge.app.ports.output.user_repository import UserRepository

_DEFAULT_CATEGORY = "기타"


class InventoryInteractor(InventoryUseCase):

    def __init__(
        self,
        users: UserRepository,
        inventory: InventoryRepository,
        foods: FoodRepository,
        categories: CategoryRepository,
    ) -> None:
        self._users = users
        self._inventory = inventory
        self._foods = foods
        self._categories = categories

    async def _resolve_food_id(self, name: str, unit: str) -> int:
        existing = await self._foods.find_by_name(name)
        if existing:
            return existing
        category_id = await self._categories.get_or_create_default(_DEFAULT_CATEGORY)
        safe_unit = unit if unit in UNIT_CHOICES else "개"
        return await self._foods.create(category_id, name, safe_unit)

    def _status_item(self, item: InventoryItemDto) -> InventoryStatusItem:
        return InventoryStatusItem(
            name=item.name,
            quantity=item.quantity,
            unit=item.unit,
            expiry_date=item.expiry_date,
            purchased_date=item.purchased_date,
            expiry_is_estimated=item.expiry_is_estimated,
            storage=item.storage,
            min_quantity=item.min_quantity,
        )

    def _resolve_dates_on_create(self, command: CreateInventoryCommand) -> CreateInventoryCommand:
        if command.expiry_date is not None:
            return command
        if command.purchased_date is not None:
            exp = expiry_from_purchase(command.name, command.purchased_date, command.storage)
            return CreateInventoryCommand(
                user_id=command.user_id,
                name=command.name,
                quantity=command.quantity,
                unit=command.unit,
                expiry_date=exp,
                purchased_date=command.purchased_date,
                expiry_is_estimated=True,
                storage=command.storage,
                min_quantity=command.min_quantity,
            )
        return CreateInventoryCommand(
            user_id=command.user_id,
            name=command.name,
            quantity=command.quantity,
            unit=command.unit,
            expiry_date=None,
            purchased_date=None,
            expiry_is_estimated=False,
            storage=command.storage,
            min_quantity=command.min_quantity,
        )

    async def estimate_expiry(self, name: str, purchased_date: date, storage: str) -> ExpiryEstimateDto:
        s = storage.strip()
        if s not in STORAGE_CHOICES:
            raise HTTPException(status_code=400, detail="보관 방식을 확인해 주세요.")
        n = name.strip()
        days = estimate_shelf_life_days(n, s)
        exp = expiry_from_purchase(n, purchased_date, s)
        return ExpiryEstimateDto(
            name=n,
            purchased_date=purchased_date,
            storage=s,
            shelf_life_days=days,
            estimated_expiry_date=exp,
            message=f"{n}은(는) 보통 구매 후 {days}일까지 ({s})",
        )

    async def list_inventory(self, user_email: str) -> InventoryListDto:
        user = await self._users.get_by_email(user_email)
        items = await self._inventory.list_by_user(user.id)
        status_items = [self._status_item(i) for i in items]
        return InventoryListDto(
            items=items,
            stats=InventoryStatsDto(
                total=len(items),
                expiring_soon=count_expiring_soon(status_items),
                low_stock=count_low_stock(status_items),
            ),
        )

    async def create_item(self, user_email: str, command: CreateInventoryCommand) -> InventoryItemDto:
        user = await self._users.get_by_email(user_email)
        resolved = self._resolve_dates_on_create(
            CreateInventoryCommand(
                user_id=user.id,
                name=command.name,
                quantity=command.quantity,
                unit=command.unit,
                expiry_date=command.expiry_date,
                purchased_date=command.purchased_date,
                expiry_is_estimated=command.expiry_date is None and command.purchased_date is not None,
                storage=command.storage,
                min_quantity=command.min_quantity,
            ),
        )
        food_id = await self._resolve_food_id(resolved.name, resolved.unit)
        item = await self._inventory.create(resolved, food_id)
        await self._inventory.commit()
        return item

    async def update_item(
        self,
        user_email: str,
        item_id: int,
        command: UpdateInventoryCommand,
    ) -> InventoryItemDto:
        user = await self._users.get_by_email(user_email)
        food_id = None
        if command.name is not None:
            current = await self._inventory.get_owned(user.id, item_id)
            food_id = await self._resolve_food_id(command.name, command.unit or current.unit)
        item = await self._inventory.update(user.id, item_id, command, food_id)
        await self._inventory.commit()
        return item

    async def consume_item(self, user_email: str, item_id: int, amount: int) -> AdjustInventoryResultDto:
        user = await self._users.get_by_email(user_email)
        current = await self._inventory.get_owned(user.id, item_id)
        item, removed = await self._inventory.adjust_quantity(user.id, item_id, -amount)
        await self._inventory.commit()
        if removed:
            return AdjustInventoryResultDto(
                item=None,
                removed=True,
                message=f"{current.name}을(를) 모두 사용했어요. 목록에서 제거했습니다.",
            )
        assert item is not None
        return AdjustInventoryResultDto(
            item=item,
            removed=False,
            message=f"{current.name} {amount}{item.unit} 사용 → 남은 수량 {format_quantity(item.quantity, item.unit)}",
        )

    async def add_quantity(self, user_email: str, item_id: int, amount: int) -> AdjustInventoryResultDto:
        user = await self._users.get_by_email(user_email)
        item, _ = await self._inventory.adjust_quantity(user.id, item_id, amount)
        await self._inventory.commit()
        assert item is not None
        return AdjustInventoryResultDto(
            item=item,
            removed=False,
            message=f"{item.name} {amount}{item.unit} 추가 → {format_quantity(item.quantity, item.unit)}",
        )

    async def delete_item(self, user_email: str, item_id: int) -> None:
        user = await self._users.get_by_email(user_email)
        await self._inventory.delete(user.id, item_id)
        await self._inventory.commit()
