from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from fridge.adapter.outbound.gemini.receipt_parser import GeminiReceiptParser
from fridge.adapter.outbound.pg.category_pg_repository import CategoryPgRepository
from fridge.adapter.outbound.pg.food_pg_repository import FoodPgRepository
from fridge.adapter.outbound.pg.inventory_pg_repository import InventoryPgRepository
from fridge.adapter.outbound.pg.receipt_pg_repository import ReceiptPgRepository
from fridge.adapter.outbound.pg.user_pg_repository import UserPgRepository
from fridge.app.ports.input.receipt_scan_use_case import ReceiptScanUseCase
from fridge.app.ports.output.category_repository import CategoryRepository
from fridge.app.ports.output.food_repository import FoodRepository
from fridge.app.ports.output.inventory_repository import InventoryRepository
from fridge.app.ports.output.receipt_parser import ReceiptParserPort
from fridge.app.ports.output.receipt_repository import ReceiptRepository
from fridge.app.ports.output.user_repository import UserRepository
from fridge.app.use_cases.receipt_scan_interactor import ReceiptScanInteractor
from core.matrix.oracle_database import get_db


def get_receipt_scan_use_case(
    db: AsyncSession = Depends(get_db),
) -> ReceiptScanUseCase:
    users: UserRepository = UserPgRepository(session=db)
    parser: ReceiptParserPort = GeminiReceiptParser()
    receipts: ReceiptRepository = ReceiptPgRepository(session=db)
    foods: FoodRepository = FoodPgRepository(session=db)
    categories: CategoryRepository = CategoryPgRepository(session=db)
    inventory: InventoryRepository = InventoryPgRepository(session=db)
    return ReceiptScanInteractor(
        users=users,
        parser=parser,
        receipts=receipts,
        foods=foods,
        categories=categories,
        inventory=inventory,
    )
