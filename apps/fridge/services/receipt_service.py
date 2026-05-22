"""영수증 파싱 결과 저장 및 inventory 반영."""

from datetime import date

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from fridge.repositories.category_repository import CategoryRepository
from fridge.repositories.food_repository import FoodRepository
from fridge.repositories.inventory_repository import InventoryRepository
from fridge.repositories.receipt_repository import ReceiptRepository
from fridge.schemas.category_schema import CategoryCreate
from fridge.schemas.food_schema import FoodCreate
from fridge.schemas.inventory_schema import InventoryCreate
from fridge.schemas.receipt_schema import ReceiptParseResult, ReceiptScanResponse, ReceiptLineResponse
from fridge.services.ingredient_logic import UNIT_CHOICES, expiry_from_purchase
from fridge.services import ingredient_service
from models.user import User

_DEFAULT_CATEGORY = "기타"


class ReceiptService:
    def __init__(self) -> None:
        self._receipts = ReceiptRepository()
        self._foods = FoodRepository()
        self._categories = CategoryRepository()
        self._inventory = InventoryRepository()

    async def _default_category_id(self, db: AsyncSession) -> int:
        cat = await self._categories.get_by_name(db, _DEFAULT_CATEGORY)
        if cat:
            return cat.id
        created = await self._categories.add(
            db,
            CategoryCreate(name=_DEFAULT_CATEGORY, sort_order=999),
        )
        return created.id

    async def _resolve_food(
        self,
        db: AsyncSession,
        line_name: str,
        default_unit: str,
    ) -> int:
        existing = await self._foods.find_by_name(db, line_name)
        if existing:
            return existing.id
        category_id = await self._default_category_id(db)
        unit = default_unit if default_unit in UNIT_CHOICES else "개"
        created = await self._foods.add(
            db,
            FoodCreate(category_id=category_id, name=line_name, default_unit=unit),
        )
        return created.id

    async def persist_parsed_receipt(
        self,
        db: AsyncSession,
        user: User,
        parsed: ReceiptParseResult,
    ) -> ReceiptScanResponse:
        if not parsed.items:
            raise HTTPException(status_code=422, detail="영수증에서 품목을 찾지 못했습니다.")

        purchased = parsed.purchased_date or date.today()
        storage = (user.default_storage or "냉장").strip()

        receipt = await self._receipts.create_receipt(
            db,
            user_id=user.id,
            store_name=parsed.store_name,
            purchased_date=purchased,
            status="parsed",
        )

        line_responses: list[ReceiptLineResponse] = []
        inventory_created = 0

        for item in parsed.items:
            food_id = await self._resolve_food(db, item.name, item.unit)
            expiry = expiry_from_purchase(item.name, purchased, storage)
            inv = await self._inventory.add(
                db,
                InventoryCreate(
                    user_id=user.id,
                    food_id=food_id,
                    quantity=item.quantity,
                    unit=item.unit,
                    expiry_date=expiry,
                    purchased_date=purchased,
                    expiry_is_estimated=True,
                    storage=storage,
                ),
            )
            inventory_created += 1
            line = await self._receipts.create_line(
                db,
                receipt_id=receipt.id,
                line_name=item.name,
                quantity=item.quantity,
                unit=item.unit,
                food_id=food_id,
                inventory_id=inv.id,
            )
            line_responses.append(
                ReceiptLineResponse(
                    id=line.id,
                    line_name=line.line_name,
                    quantity=line.quantity,
                    unit=line.unit,
                    food_id=line.food_id,
                    inventory_id=line.inventory_id,
                ),
            )

        await db.commit()

        return ReceiptScanResponse(
            receipt_id=receipt.id,
            store_name=receipt.store_name,
            purchased_date=receipt.purchased_date,
            status=receipt.status,
            lines=line_responses,
            inventory_created=inventory_created,
        )

    async def scan_image(
        self,
        db: AsyncSession,
        user_email: str,
        image_bytes: bytes,
        mime_type: str,
    ) -> ReceiptScanResponse:
        from fridge.services.receipt_parse_service import parse_receipt_image

        user = await ingredient_service.user_from_email(db, user_email)
        parsed = parse_receipt_image(image_bytes, mime_type)
        return await self.persist_parsed_receipt(db, user, parsed)
