from datetime import date

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from fridge.schemas.ingredient_schema import IngredientItemCreate, IngredientItemResponse
from fridge.services.ingredient_logic import (
    compute_status,
    estimate_shelf_life_days,
    expiry_from_purchase,
    format_quantity,
)
from models.ingredient_manager import IngredientManager
from models.user import User


def resolve_dates_on_create(body: IngredientItemCreate) -> tuple[date | None, date | None, bool]:
    """유통기한 직접 입력 우선, 없으면 구매일로 추정."""
    if body.expiry_date is not None:
        return body.expiry_date, body.purchased_date, False
    if body.purchased_date is not None:
        exp = expiry_from_purchase(body.name, body.purchased_date, body.storage)
        return exp, body.purchased_date, True
    return None, None, False


def shelf_life_hint(item: IngredientManager) -> int | None:
    if item.purchased_date and item.expiry_date and item.expiry_is_estimated:
        return (item.expiry_date - item.purchased_date).days
    if item.expiry_is_estimated and item.purchased_date:
        return estimate_shelf_life_days(item.name, item.storage)
    return None


def to_response(item: IngredientManager) -> IngredientItemResponse:
    return IngredientItemResponse(
        id=item.id,
        name=item.name,
        quantity=item.quantity,
        unit=item.unit,
        quantity_label=format_quantity(item.quantity, item.unit),
        expiry_date=item.expiry_date,
        purchased_date=item.purchased_date,
        expiry_is_estimated=item.expiry_is_estimated,
        shelf_life_days=shelf_life_hint(item),
        storage=item.storage,
        min_quantity=item.min_quantity,
        status=compute_status(item),
    )


async def user_from_email(db: AsyncSession, email: str) -> User:
    e = email.strip().lower()
    if not e or "@" not in e:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
    result = await db.execute(
        select(User).where(func.lower(User.email) == e).limit(1),
    )
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=401, detail="등록된 회원이 아닙니다. 로그인해 주세요.")
    return user


async def get_owned_item(
    db: AsyncSession,
    user_id: int,
    item_id: int,
) -> IngredientManager:
    result = await db.execute(
        select(IngredientManager).where(
            IngredientManager.id == item_id,
            IngredientManager.user_id == user_id,
        ),
    )
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="식재료를 찾을 수 없습니다.")
    return item
