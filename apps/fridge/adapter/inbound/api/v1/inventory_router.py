from datetime import date

from fastapi import APIRouter, Depends, Header, Query

from fridge.adapter.inbound.api.schemas.inventory_schemas import (
    InventoryAdjustResponse,
    InventoryExpiryEstimateResponse,
    InventoryItemCreate,
    InventoryItemResponse,
    InventoryItemUpdate,
    InventoryListResponse,
    InventoryQuantityAdjustBody,
)
from fridge.adapter.inbound.api.schemas.mappers import (
    to_adjust_response,
    to_expiry_estimate_response,
    to_inventory_item_response,
    to_inventory_list_response,
)
from fridge.app.dtos.inventory_dto import CreateInventoryCommand, UpdateInventoryCommand
from fridge.app.ports.input.inventory_use_case import InventoryUseCase
from fridge.dependencies.inventory import get_inventory_use_case

inventory_router = APIRouter(prefix="/inventory", tags=["inventory"])


@inventory_router.get("/estimate-expiry", response_model=InventoryExpiryEstimateResponse)
async def estimate_expiry(
    name: str = Query(..., min_length=1),
    purchased_date: date = Query(..., alias="purchasedDate"),
    storage: str = Query(default="냉장"),
    inventory: InventoryUseCase = Depends(get_inventory_use_case),
) -> InventoryExpiryEstimateResponse:
    return to_expiry_estimate_response(
        await inventory.estimate_expiry(name, purchased_date, storage),
    )


@inventory_router.get("", response_model=InventoryListResponse)
async def list_inventory(
    x_user_email: str = Header(..., alias="X-User-Email"),
    inventory: InventoryUseCase = Depends(get_inventory_use_case),
) -> InventoryListResponse:
    return to_inventory_list_response(await inventory.list_inventory(x_user_email))


@inventory_router.post("", response_model=InventoryItemResponse, status_code=201)
async def create_inventory_item(
    body: InventoryItemCreate,
    x_user_email: str = Header(..., alias="X-User-Email"),
    inventory: InventoryUseCase = Depends(get_inventory_use_case),
) -> InventoryItemResponse:
    item = await inventory.create_item(
        x_user_email,
        CreateInventoryCommand(
            user_id=0,
            name=body.name,
            quantity=body.quantity,
            unit=body.unit,
            expiry_date=body.expiry_date,
            purchased_date=body.purchased_date,
            expiry_is_estimated=body.expiry_date is None and body.purchased_date is not None,
            storage=body.storage,
            min_quantity=body.min_quantity,
        ),
    )
    return to_inventory_item_response(item)


@inventory_router.put("/{item_id}", response_model=InventoryItemResponse)
async def update_inventory_item(
    item_id: int,
    body: InventoryItemUpdate,
    x_user_email: str = Header(..., alias="X-User-Email"),
    inventory: InventoryUseCase = Depends(get_inventory_use_case),
) -> InventoryItemResponse:
    item = await inventory.update_item(
        x_user_email,
        item_id,
        UpdateInventoryCommand(
            name=body.name,
            quantity=body.quantity,
            unit=body.unit,
            expiry_date=body.expiry_date,
            storage=body.storage,
            min_quantity=body.min_quantity,
        ),
    )
    return to_inventory_item_response(item)


@inventory_router.post("/{item_id}/consume", response_model=InventoryAdjustResponse)
async def consume_inventory_item(
    item_id: int,
    body: InventoryQuantityAdjustBody = InventoryQuantityAdjustBody(),
    x_user_email: str = Header(..., alias="X-User-Email"),
    inventory: InventoryUseCase = Depends(get_inventory_use_case),
) -> InventoryAdjustResponse:
    return to_adjust_response(await inventory.consume_item(x_user_email, item_id, body.amount))


@inventory_router.post("/{item_id}/add", response_model=InventoryAdjustResponse)
async def add_inventory_quantity(
    item_id: int,
    body: InventoryQuantityAdjustBody = InventoryQuantityAdjustBody(),
    x_user_email: str = Header(..., alias="X-User-Email"),
    inventory: InventoryUseCase = Depends(get_inventory_use_case),
) -> InventoryAdjustResponse:
    return to_adjust_response(await inventory.add_quantity(x_user_email, item_id, body.amount))


@inventory_router.delete("/{item_id}", status_code=204)
async def delete_inventory_item(
    item_id: int,
    x_user_email: str = Header(..., alias="X-User-Email"),
    inventory: InventoryUseCase = Depends(get_inventory_use_case),
) -> None:
    await inventory.delete_item(x_user_email, item_id)
