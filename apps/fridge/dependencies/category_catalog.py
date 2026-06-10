from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from fridge.adapter.outbound.pg.category_pg_repository import CategoryPgRepository
from fridge.app.ports.input.category_catalog_use_case import CategoryCatalogUseCase
from fridge.app.ports.output.category_repository import CategoryRepository
from fridge.app.use_cases.category_catalog_interactor import CategoryCatalogInteractor
from core.matrix.oracle_database import get_db


def get_category_catalog_use_case(
    db: AsyncSession = Depends(get_db),
) -> CategoryCatalogUseCase:
    categories: CategoryRepository = CategoryPgRepository(session=db)
    return CategoryCatalogInteractor(categories=categories)
