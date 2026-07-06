from __future__ import annotations

import logging
from datetime import date, timedelta

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from users.adapter.user import User as UserOrm

from fridge.adapter.outbound.orm.foods_orm import FoodsOrm
from fridge.adapter.outbound.orm.inventory_orm import InventoryOrm
from fridge.app.dtos.inventory_dto import (
    AdjustInventoryCommand,
    CreateInventoryCommand,
    InventoryAdjustResultDto,
    InventoryExpiryResponse,
    InventoryItemDto,
    InventoryListDto,
    InventoryQuery,
    InventoryStatsDto,
)
from fridge.app.ports.output.inventory_repository import InventoryRepository

logger = logging.getLogger(__name__)

# 식품별 보관 방법에 따른 유통기한 기본값 (일)
_SHELF_LIFE: dict[str, dict[str, int]] = {
    "우유": {"냉장": 7, "냉동": 30, "실온": 1},
    "계란": {"냉장": 21, "냉동": 60, "실온": 7},
    "두부": {"냉장": 5, "냉동": 30, "실온": 1},
    "돼지고기": {"냉장": 3, "냉동": 90, "실온": 0},
    "소고기": {"냉장": 3, "냉동": 90, "실온": 0},
    "닭고기": {"냉장": 2, "냉동": 60, "실온": 0},
    "생선": {"냉장": 2, "냉동": 60, "실온": 0},
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
    "두유": {"냉장": 7, "냉동": 30, "실온": 1},
    "요구르트": {"냉장": 14, "냉동": 30, "실온": 0},
    "치즈": {"냉장": 30, "냉동": 90, "실온": 0},
    "버터": {"냉장": 30, "냉동": 90, "실온": 1},
    "된장": {"냉장": 180, "냉동": 365, "실온": 90},
    "간장": {"냉장": 365, "냉동": 365, "실온": 180},
    "고추장": {"냉장": 180, "냉동": 365, "실온": 90},
    "밥": {"냉장": 3, "냉동": 30, "실온": 1},
}
_DEFAULT_SHELF_LIFE = {"냉장": 7, "냉동": 30, "실온": 3}


def _shelf_life_days(name: str, storage: str) -> int:
    for key, val in _SHELF_LIFE.items():
        if key in name:
            return val.get(storage, _DEFAULT_SHELF_LIFE.get(storage, 7))
    return _DEFAULT_SHELF_LIFE.get(storage, 7)


def _compute_status(expiry_date: date | None) -> str:
    if expiry_date is None:
        return "ok"
    today = date.today()
    if expiry_date < today:
        return "expired"
    if expiry_date <= today + timedelta(days=3):
        return "expiring_soon"
    return "ok"


def _to_dto(orm: InventoryOrm, food_name: str) -> InventoryItemDto:
    qty = orm.quantity or 0
    unit = orm.unit or "개"
    expiry = str(orm.expiry_date) if orm.expiry_date else None
    purchased = str(orm.purchased_date) if orm.purchased_date else None
    storage = orm.storage or "냉장"
    days = _shelf_life_days(food_name, storage)
    status = _compute_status(
        orm.expiry_date
        if isinstance(orm.expiry_date, date)
        else (date.fromisoformat(str(orm.expiry_date)) if orm.expiry_date else None)
    )
    return InventoryItemDto(
        id=orm.id,
        name=food_name,
        quantity=qty,
        unit=unit,
        quantity_label=f"{qty} {unit}",
        expiry_date=expiry,
        purchased_date=purchased,
        expiry_is_estimated=bool(orm.expiry_is_estimated),
        shelf_life_days=days,
        storage=storage,
        min_quantity=1,
        status=status,
    )


class InventoryPgRepository(InventoryRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _get_user_id(self, email: str) -> int:
        result = await self.session.execute(
            select(UserOrm).where(UserOrm.email == email)
        )  # type: ignore[attr-defined]
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
        return user.id

    async def _get_or_create_food(self, name: str) -> int:
        result = await self.session.execute(
            select(FoodsOrm).where(FoodsOrm.name == name)
        )
        food = result.scalar_one_or_none()
        if food:
            return food.id
        new_food = FoodsOrm(name=name, default_unit="개")
        self.session.add(new_food)
        await self.session.flush()
        return new_food.id

    async def get_urgent_items(self, query: InventoryQuery) -> InventoryExpiryResponse:
        return InventoryExpiryResponse(id=1, food_id=query.food_id)

    async def list_by_user_email(self, user_email: str) -> InventoryListDto:
        user_id = await self._get_user_id(user_email)
        result = await self.session.execute(
            select(InventoryOrm, FoodsOrm.name)
            .join(FoodsOrm, InventoryOrm.food_id == FoodsOrm.id)
            .where(InventoryOrm.user_id == user_id)
            .order_by(InventoryOrm.expiry_date.asc().nulls_last())
        )
        rows = result.all()
        items = [_to_dto(orm, name or "알 수 없음") for orm, name in rows]
        expiring_soon = sum(1 for i in items if i.status == "expiring_soon")
        low_stock = sum(1 for i in items if i.quantity <= i.min_quantity)
        return InventoryListDto(
            items=items,
            stats=InventoryStatsDto(
                total=len(items), expiring_soon=expiring_soon, low_stock=low_stock
            ),
        )

    async def create(self, cmd: CreateInventoryCommand) -> InventoryItemDto:
        user_id = await self._get_user_id(cmd.user_email)
        food_id = await self._get_or_create_food(cmd.name)
        expiry_date = date.fromisoformat(cmd.expiry_date) if cmd.expiry_date else None
        purchased_date = (
            date.fromisoformat(cmd.purchased_date) if cmd.purchased_date else None
        )
        is_estimated = expiry_date is None
        if not expiry_date and purchased_date:
            days = _shelf_life_days(cmd.name, cmd.storage)
            expiry_date = purchased_date + timedelta(days=days)
            is_estimated = True
        new_item = InventoryOrm(
            user_id=user_id,
            food_id=food_id,
            quantity=cmd.quantity,
            unit=cmd.unit,
            expiry_date=expiry_date,
            purchased_date=purchased_date,
            expiry_is_estimated=is_estimated,
            storage=cmd.storage,
        )
        self.session.add(new_item)
        await self.session.commit()
        await self.session.refresh(new_item)
        return _to_dto(new_item, cmd.name)

    async def delete(self, user_email: str, item_id: int) -> None:
        user_id = await self._get_user_id(user_email)
        result = await self.session.execute(
            select(InventoryOrm).where(
                InventoryOrm.id == item_id, InventoryOrm.user_id == user_id
            )
        )
        item = result.scalar_one_or_none()
        if not item:
            raise HTTPException(status_code=404, detail="재료를 찾을 수 없습니다.")
        await self.session.delete(item)
        await self.session.commit()

    async def _get_item_with_food(
        self, user_email: str, item_id: int
    ) -> tuple[InventoryOrm, str]:
        user_id = await self._get_user_id(user_email)
        result = await self.session.execute(
            select(InventoryOrm, FoodsOrm.name)
            .join(FoodsOrm, InventoryOrm.food_id == FoodsOrm.id)
            .where(InventoryOrm.id == item_id, InventoryOrm.user_id == user_id)
        )
        row = result.first()
        if not row:
            raise HTTPException(status_code=404, detail="재료를 찾을 수 없습니다.")
        return row[0], row[1] or "알 수 없음"

    async def consume(self, cmd: AdjustInventoryCommand) -> InventoryAdjustResultDto:
        item, food_name = await self._get_item_with_food(cmd.user_email, cmd.item_id)
        new_qty = (item.quantity or 0) - cmd.amount
        if new_qty <= 0:
            await self.session.delete(item)
            await self.session.commit()
            return InventoryAdjustResultDto(
                item=None, removed=True, message=f"{food_name} 소진 완료!"
            )
        item.quantity = new_qty
        await self.session.commit()
        await self.session.refresh(item)
        return InventoryAdjustResultDto(
            item=_to_dto(item, food_name), removed=False, message="수량이 줄었습니다."
        )

    async def add_quantity(
        self, cmd: AdjustInventoryCommand
    ) -> InventoryAdjustResultDto:
        item, food_name = await self._get_item_with_food(cmd.user_email, cmd.item_id)
        item.quantity = (item.quantity or 0) + cmd.amount
        await self.session.commit()
        await self.session.refresh(item)
        return InventoryAdjustResultDto(
            item=_to_dto(item, food_name), removed=False, message="수량이 늘었습니다."
        )
