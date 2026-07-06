from __future__ import annotations

from fastapi import APIRouter, Depends, Header, Query
from pydantic import BaseModel

from fridge.app.dtos.inventory_dto import (
    AdjustInventoryCommand,
    CreateInventoryCommand,
)
from fridge.app.ports.input.inventory_use_case import InventoryUseCase
from fridge.dependencies.inventory_provider import get_inventory_use_case

inventory_router = APIRouter(prefix="/inventory", tags=["inventory"])


class CreateItemBody(BaseModel):
    name: str
    quantity: int = 1
    unit: str = "개"
    expiry_date: str | None = None
    purchased_date: str | None = None
    storage: str = "냉장"
    min_quantity: int = 1


class AdjustBody(BaseModel):
    amount: int = 1


@inventory_router.get("/estimate-expiry")
async def estimate_expiry(
    name: str = Query(...),
    purchasedDate: str = Query(...),
    storage: str = Query(...),
    use_case: InventoryUseCase = Depends(get_inventory_use_case),
):
    result = await use_case.estimate_expiry(name, purchasedDate, storage)
    return vars(result)


@inventory_router.get("")
async def list_inventory(
    x_user_email: str = Header(...),
    use_case: InventoryUseCase = Depends(get_inventory_use_case),
):
    result = await use_case.list_inventory(x_user_email)
    return {
        "items": [vars(i) for i in result.items],
        "stats": vars(result.stats),
    }


@inventory_router.post("")
async def create_item(
    body: CreateItemBody,
    x_user_email: str = Header(...),
    use_case: InventoryUseCase = Depends(get_inventory_use_case),
):
    cmd = CreateInventoryCommand(
        user_email=x_user_email,
        name=body.name,
        quantity=body.quantity,
        unit=body.unit,
        expiry_date=body.expiry_date,
        purchased_date=body.purchased_date,
        storage=body.storage,
        min_quantity=body.min_quantity,
    )
    item = await use_case.create_item(cmd)
    return vars(item)


@inventory_router.delete("/{item_id}", status_code=204)
async def delete_item(
    item_id: int,
    x_user_email: str = Header(...),
    use_case: InventoryUseCase = Depends(get_inventory_use_case),
):
    await use_case.delete_item(x_user_email, item_id)


@inventory_router.post("/{item_id}/consume")
async def consume_item(
    item_id: int,
    body: AdjustBody,
    x_user_email: str = Header(...),
    use_case: InventoryUseCase = Depends(get_inventory_use_case),
):
    cmd = AdjustInventoryCommand(
        user_email=x_user_email, item_id=item_id, amount=body.amount
    )
    result = await use_case.consume_item(cmd)
    return {
        "item": vars(result.item) if result.item else None,
        "removed": result.removed,
        "message": result.message,
    }


@inventory_router.post("/{item_id}/add")
async def add_quantity(
    item_id: int,
    body: AdjustBody,
    x_user_email: str = Header(...),
    use_case: InventoryUseCase = Depends(get_inventory_use_case),
):
    cmd = AdjustInventoryCommand(
        user_email=x_user_email, item_id=item_id, amount=body.amount
    )
    result = await use_case.add_quantity(cmd)
    return {
        "item": vars(result.item) if result.item else None,
        "removed": result.removed,
        "message": result.message,
    }
