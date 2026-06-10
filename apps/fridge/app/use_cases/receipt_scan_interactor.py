from __future__ import annotations

from datetime import date

from fastapi import HTTPException

from fridge.app.use_cases._shelf_life import UNIT_CHOICES, expiry_from_purchase
from fridge.app.dtos.inventory_dto import CreateInventoryCommand
from fridge.app.dtos.receipt_dto import ReceiptParseResultDto, ReceiptScanResultDto
from fridge.app.ports.input.receipt_scan_use_case import ReceiptScanUseCase
from fridge.app.ports.output.category_repository import CategoryRepository
from fridge.app.ports.output.food_repository import FoodRepository
from fridge.app.ports.output.inventory_repository import InventoryRepository
from fridge.app.ports.output.receipt_parser import ReceiptParserPort
from fridge.app.ports.output.receipt_repository import ReceiptRepository
from fridge.app.ports.output.user_repository import UserRepository

_DEFAULT_CATEGORY = "기타"


class ReceiptScanInteractor(ReceiptScanUseCase):

    def __init__(
        self,
        users: UserRepository,
        parser: ReceiptParserPort,
        receipts: ReceiptRepository,
        foods: FoodRepository,
        categories: CategoryRepository,
        inventory: InventoryRepository,
    ) -> None:
        self._users = users
        self._parser = parser
        self._receipts = receipts
        self._foods = foods
        self._categories = categories
        self._inventory = inventory

    async def _resolve_food_id(self, line_name: str, unit: str) -> int:
        existing = await self._foods.find_by_name(line_name)
        if existing:
            return existing
        category_id = await self._categories.get_or_create_default(_DEFAULT_CATEGORY)
        safe_unit = unit if unit in UNIT_CHOICES else "개"
        return await self._foods.create(category_id, line_name, safe_unit)

    async def _persist(self, user_id: int, storage: str, parsed: ReceiptParseResultDto) -> ReceiptScanResultDto:
        if not parsed.items:
            raise HTTPException(status_code=422, detail="영수증에서 품목을 찾지 못했습니다.")

        purchased = parsed.purchased_date or date.today()
        receipt_id = await self._receipts.create_receipt(
            user_id,
            parsed.store_name,
            purchased,
            "parsed",
        )

        lines = []
        inventory_created = 0

        for item in parsed.items:
            food_id = await self._resolve_food_id(item.name, item.unit)
            expiry = expiry_from_purchase(item.name, purchased, storage)
            inv = await self._inventory.create(
                CreateInventoryCommand(
                    user_id=user_id,
                    name=item.name,
                    quantity=item.quantity,
                    unit=item.unit,
                    expiry_date=expiry,
                    purchased_date=purchased,
                    expiry_is_estimated=True,
                    storage=storage,
                ),
                food_id,
            )
            inventory_created += 1
            line = await self._receipts.create_line(
                receipt_id,
                item.name,
                item.quantity,
                item.unit,
                food_id,
                inv.id,
            )
            lines.append(line)

        await self._receipts.commit()

        return ReceiptScanResultDto(
            receipt_id=receipt_id,
            store_name=parsed.store_name,
            purchased_date=purchased,
            status="parsed",
            lines=lines,
            inventory_created=inventory_created,
        )

    async def scan_receipt(
        self,
        user_email: str,
        image_bytes: bytes,
        mime_type: str,
    ) -> ReceiptScanResultDto:
        user = await self._users.get_by_email(user_email)
        parsed = self._parser.parse(image_bytes, mime_type)
        return await self._persist(user.id, user.default_storage, parsed)
