from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from fridge.adapter.outbound.pg.inventory_pg_repository import InventoryPgRepository
from fridge.app.ports.input.inventory_use_case import InventoryUseCase
from fridge.app.ports.output.inventory_repository import InventoryRepository
from fridge.app.use_cases.inventory_interactor import InventoryInteractor


def get_inventory_repository(
    db: AsyncSession = Depends(get_db),
) -> InventoryPgRepository:
    return InventoryPgRepository(session=db)


def get_inventory_use_case(
    repository: InventoryRepository = Depends(get_inventory_repository),
) -> InventoryUseCase:
    return InventoryInteractor(repository=repository)
