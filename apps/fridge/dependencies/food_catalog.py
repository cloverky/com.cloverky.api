from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from fridge.adapter.outbound.pg.food_pg_repository import FoodPgRepository
from fridge.app.ports.input.food_catalog_use_case import FoodCatalogUseCase
from fridge.app.ports.output.food_repository import FoodRepository
from fridge.app.use_cases.food_catalog_interactor import FoodCatalogInteractor
from core.matrix.oracle_database import get_db


def get_food_catalog_use_case(
    db: AsyncSession = Depends(get_db),
) -> FoodCatalogUseCase:
    foods: FoodRepository = FoodPgRepository(session=db)
    return FoodCatalogInteractor(foods=foods)
