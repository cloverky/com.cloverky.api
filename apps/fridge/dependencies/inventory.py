from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from fridge.adapter.outbound.pg.category_pg_repository import CategoryPgRepository
from fridge.adapter.outbound.pg.food_pg_repository import FoodPgRepository
from fridge.adapter.outbound.pg.inventory_pg_repository import InventoryPgRepository
from fridge.adapter.outbound.pg.user_pg_repository import UserPgRepository
from fridge.app.ports.input.inventory_use_case import InventoryUseCase
from fridge.app.ports.output.category_repository import CategoryRepository
from fridge.app.ports.output.food_repository import FoodRepository
from fridge.app.ports.output.inventory_repository import InventoryRepository
from fridge.app.ports.output.user_repository import UserRepository
from fridge.app.use_cases.inventory_interactor import InventoryInteractor
from core.matrix.oracle_database import get_db


def get_inventory_use_case(
    db: AsyncSession = Depends(get_db),
) -> InventoryUseCase:
    users: UserRepository = UserPgRepository(session=db)
    inventory: InventoryRepository = InventoryPgRepository(session=db)
    foods: FoodRepository = FoodPgRepository(session=db)
    categories: CategoryRepository = CategoryPgRepository(session=db)
    return InventoryInteractor(
        users=users,
        inventory=inventory,
        foods=foods,
        categories=categories,
    )
