from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from fridge.app.dtos.inventory_dto import CreateInventoryCommand, InventoryItemDto, UpdateInventoryCommand
from fridge.app.ports.output.inventory_repository import InventoryRepository
from fridge.adapter.outbound.orm.food_orm import FoodOrm
from fridge.adapter.outbound.orm.inventory_orm import InventoryOrm


class InventoryPgRepository(InventoryRepository):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _to_dto(self, inv: InventoryOrm, food: FoodOrm) -> InventoryItemDto:
        return InventoryItemDto(
            id=inv.id,
            food_id=inv.food_id,
            name=food.name,
            quantity=inv.quantity,
            unit=inv.unit,
            expiry_date=inv.expiry_date,
            purchased_date=inv.purchased_date,
            expiry_is_estimated=inv.expiry_is_estimated,
            storage=inv.storage,
        )

    async def _get_row(self, user_id: int, item_id: int) -> tuple[InventoryOrm, FoodOrm]:
        result = await self._session.execute(
            select(InventoryOrm, FoodOrm)
            .join(FoodOrm, InventoryOrm.food_id == FoodOrm.id)
            .where(
                InventoryOrm.id == item_id,
                InventoryOrm.user_id == user_id,
            )
            .limit(1),
        )
        row = result.one_or_none()
        if row is None:
            raise HTTPException(status_code=404, detail="식재료를 찾을 수 없습니다.")
        return row[0], row[1]

    async def list_by_user(self, user_id: int) -> list[InventoryItemDto]:
        result = await self._session.execute(
            select(InventoryOrm, FoodOrm)
            .join(FoodOrm, InventoryOrm.food_id == FoodOrm.id)
            .where(InventoryOrm.user_id == user_id)
            .order_by(
                InventoryOrm.expiry_date.asc().nulls_last(),
                InventoryOrm.id.desc(),
            ),
        )
        return [self._to_dto(inv, food) for inv, food in result.all()]

    async def get_owned(self, user_id: int, item_id: int) -> InventoryItemDto:
        inv, food = await self._get_row(user_id, item_id)
        return self._to_dto(inv, food)

    async def create(self, command: CreateInventoryCommand, food_id: int) -> InventoryItemDto:
        row = InventoryOrm(
            user_id=command.user_id,
            food_id=food_id,
            quantity=command.quantity,
            unit=command.unit,
            expiry_date=command.expiry_date,
            purchased_date=command.purchased_date,
            expiry_is_estimated=command.expiry_is_estimated,
            storage=command.storage,
        )
        self._session.add(row)
        await self._session.flush()
        await self._session.refresh(row)
        food_result = await self._session.execute(
            select(FoodOrm).where(FoodOrm.id == food_id).limit(1),
        )
        food = food_result.scalar_one()
        return self._to_dto(row, food)

    async def update(
        self,
        user_id: int,
        item_id: int,
        command: UpdateInventoryCommand,
        food_id: int | None = None,
    ) -> InventoryItemDto:
        inv, food = await self._get_row(user_id, item_id)
        if command.quantity is not None:
            inv.quantity = command.quantity
        if command.unit is not None:
            inv.unit = command.unit
        if command.expiry_date is not None:
            inv.expiry_date = command.expiry_date
        if command.storage is not None:
            inv.storage = command.storage
        if food_id is not None:
            inv.food_id = food_id
            food_result = await self._session.execute(
                select(FoodOrm).where(FoodOrm.id == food_id).limit(1),
            )
            food = food_result.scalar_one()
        await self._session.flush()
        await self._session.refresh(inv)
        return self._to_dto(inv, food)

    async def adjust_quantity(
        self,
        user_id: int,
        item_id: int,
        delta: int,
    ) -> tuple[InventoryItemDto | None, bool]:
        inv, food = await self._get_row(user_id, item_id)
        new_qty = inv.quantity + delta
        if new_qty <= 0:
            await self._session.execute(
                delete(InventoryOrm).where(
                    InventoryOrm.id == item_id,
                    InventoryOrm.user_id == user_id,
                ),
            )
            await self._session.flush()
            return None, True
        inv.quantity = new_qty
        await self._session.flush()
        await self._session.refresh(inv)
        return self._to_dto(inv, food), False

    async def delete(self, user_id: int, item_id: int) -> None:
        await self._get_row(user_id, item_id)
        await self._session.execute(
            delete(InventoryOrm).where(
                InventoryOrm.id == item_id,
                InventoryOrm.user_id == user_id,
            ),
        )
        await self._session.flush()

    async def commit(self) -> None:
        await self._session.commit()
