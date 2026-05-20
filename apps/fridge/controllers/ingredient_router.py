from datetime import date

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from fridge.models.database import get_db
from fridge.schemas.ingredient_schema import (
    IngredientAdjustResponse,
    IngredientExpiryEstimateResponse,
    IngredientItemCreate,
    IngredientItemResponse,
    IngredientItemUpdate,
    IngredientListResponse,
    IngredientQuantityAdjustBody,
    IngredientStatsResponse,
)
from fridge.services import ingredient_service
from fridge.services.ingredient_logic import (
    STORAGE_CHOICES,
    count_expiring_soon,
    count_low_stock,
    estimate_shelf_life_days,
    expiry_from_purchase,
    format_quantity,
)
from models.ingredient_manager import IngredientManager

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("/estimate-expiry", response_model=IngredientExpiryEstimateResponse)
async def estimate_expiry(
    name: str = Query(..., min_length=1),
    purchased_date: date = Query(..., alias="purchasedDate"),
    storage: str = Query(default="냉장"),
) -> IngredientExpiryEstimateResponse:
    """구매일만 알 때 유통기한 미리보기 (로그인 불필요)."""
    s = storage.strip()
    if s not in STORAGE_CHOICES:
        raise HTTPException(status_code=400, detail="보관 방식을 확인해 주세요.")
    n = name.strip()
    days = estimate_shelf_life_days(n, s)
    exp = expiry_from_purchase(n, purchased_date, s)
    return IngredientExpiryEstimateResponse(
        name=n,
        purchased_date=purchased_date,
        storage=s,
        shelf_life_days=days,
        estimated_expiry_date=exp,
        message=f"{n}은(는) 보통 구매 후 {days}일까지 ({s})",
    )


@router.get("", response_model=IngredientListResponse)
async def list_inventory(
    x_user_email: str = Header(..., alias="X-User-Email"),
    db: AsyncSession = Depends(get_db),
) -> IngredientListResponse:
    user = await ingredient_service.user_from_email(db, x_user_email)
    result = await db.execute(
        select(IngredientManager)
        .where(IngredientManager.user_id == user.id)
        .order_by(
            IngredientManager.expiry_date.asc().nulls_last(),
            IngredientManager.id.desc(),
        ),
    )
    items = list(result.scalars().all())
    responses = [ingredient_service.to_response(i) for i in items]
    return IngredientListResponse(
        items=responses,
        stats=IngredientStatsResponse(
            total=len(items),
            expiring_soon=count_expiring_soon(items),
            low_stock=count_low_stock(items),
        ),
    )


@router.post("", response_model=IngredientItemResponse, status_code=201)
async def create_inventory_item(
    body: IngredientItemCreate,
    x_user_email: str = Header(..., alias="X-User-Email"),
    db: AsyncSession = Depends(get_db),
) -> IngredientItemResponse:
    user = await ingredient_service.user_from_email(db, x_user_email)
    expiry_date, purchased_date, is_estimated = ingredient_service.resolve_dates_on_create(body)
    if body.expiry_date and body.purchased_date and not is_estimated:
        purchased_date = body.purchased_date
    item = IngredientManager(
        user_id=user.id,
        name=body.name,
        quantity=body.quantity,
        unit=body.unit,
        expiry_date=expiry_date,
        purchased_date=purchased_date,
        expiry_is_estimated=is_estimated,
        storage=body.storage,
        min_quantity=body.min_quantity,
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return ingredient_service.to_response(item)


@router.put("/{item_id}", response_model=IngredientItemResponse)
async def update_inventory_item(
    item_id: int,
    body: IngredientItemUpdate,
    x_user_email: str = Header(..., alias="X-User-Email"),
    db: AsyncSession = Depends(get_db),
) -> IngredientItemResponse:
    user = await ingredient_service.user_from_email(db, x_user_email)
    item = await ingredient_service.get_owned_item(db, user.id, item_id)
    data = body.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(item, key, value)
    await db.commit()
    await db.refresh(item)
    return ingredient_service.to_response(item)


@router.post("/{item_id}/consume", response_model=IngredientAdjustResponse)
async def consume_inventory_item(
    item_id: int,
    body: IngredientQuantityAdjustBody = IngredientQuantityAdjustBody(),
    x_user_email: str = Header(..., alias="X-User-Email"),
    db: AsyncSession = Depends(get_db),
) -> IngredientAdjustResponse:
    """하나씩 먹었을 때 수량만 줄입니다. 0 이하면 목록에서 제거합니다."""
    user = await ingredient_service.user_from_email(db, x_user_email)
    item = await ingredient_service.get_owned_item(db, user.id, item_id)
    name = item.name
    new_qty = item.quantity - body.amount

    if new_qty <= 0:
        await db.execute(
            delete(IngredientManager).where(
                IngredientManager.id == item_id,
                IngredientManager.user_id == user.id,
            ),
        )
        await db.commit()
        return IngredientAdjustResponse(
            removed=True,
            message=f"{name}을(를) 모두 사용했어요. 목록에서 제거했습니다.",
        )

    item.quantity = new_qty
    await db.commit()
    await db.refresh(item)
    label = format_quantity(item.quantity, item.unit)
    return IngredientAdjustResponse(
        item=ingredient_service.to_response(item),
        message=f"{name} {body.amount}{item.unit} 사용 → 남은 수량 {label}",
    )


@router.post("/{item_id}/add", response_model=IngredientAdjustResponse)
async def add_inventory_quantity(
    item_id: int,
    body: IngredientQuantityAdjustBody = IngredientQuantityAdjustBody(),
    x_user_email: str = Header(..., alias="X-User-Email"),
    db: AsyncSession = Depends(get_db),
) -> IngredientAdjustResponse:
    """장보기 등으로 수량을 늘립니다."""
    user = await ingredient_service.user_from_email(db, x_user_email)
    item = await ingredient_service.get_owned_item(db, user.id, item_id)
    item.quantity = item.quantity + body.amount
    await db.commit()
    await db.refresh(item)
    label = format_quantity(item.quantity, item.unit)
    return IngredientAdjustResponse(
        item=ingredient_service.to_response(item),
        message=f"{item.name} {body.amount}{item.unit} 추가 → {label}",
    )


@router.delete("/{item_id}", status_code=204)
async def delete_inventory_item(
    item_id: int,
    x_user_email: str = Header(..., alias="X-User-Email"),
    db: AsyncSession = Depends(get_db),
) -> None:
    user = await ingredient_service.user_from_email(db, x_user_email)
    await ingredient_service.get_owned_item(db, user.id, item_id)
    await db.execute(
        delete(IngredientManager).where(
            IngredientManager.id == item_id,
            IngredientManager.user_id == user.id,
        ),
    )
    await db.commit()
