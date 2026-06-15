from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from clover.apps.fridge.adapter.outbound.pg.foods_pg_repository import FoodsPgRepository
from clover.apps.fridge.app.ports.output.foods_repository import FoodsRepository
from clover.core.matrix.grid_oracle_database_manager import get_db
from clover.apps.fridge.app.ports.input.foods_use_case import FoodsUseCase
from clover.apps.fridge.app.use_cases.foods_interactor import FoodsInteractor


def get_foods_repository(
        db: AsyncSession = Depends(get_db)
) -> FoodsPgRepository:
        return FoodsPgRepository(session=db)

def get_foods_use_case(
        repository: FoodsRepository = Depends(get_foods_repository)
) -> FoodsUseCase:
        return FoodsInteractor(repository=repository)
