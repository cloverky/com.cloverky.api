from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from clover.apps.fridge.adapter.outbound.pg.category_pg_repository import CategoryPgRepository
from clover.apps.fridge.app.ports.output.category_repository import CategoryRepository
from clover.core.matrix.grid_oracle_database_manager import get_db
from clover.apps.fridge.app.ports.input.category_use_case import CategoryUseCase
from clover.apps.fridge.app.use_cases.category_interactor import CategoryInteractor


def get_category_repository(
        db: AsyncSession = Depends(get_db)
) -> CategoryPgRepository:
        return CategoryPgRepository(session=db)

def get_category_use_case(
        repository: CategoryRepository = Depends(get_category_repository)
) -> CategoryUseCase:
        return CategoryInteractor(repository=repository)
