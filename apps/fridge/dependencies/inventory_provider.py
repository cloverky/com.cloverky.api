from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from clover.apps.fridge.adapter.outbound.pg.inventory_pg_repository import InventoryPgRepository
from clover.apps.fridge.app.ports.output.inventory_repository import InventoryRepository
from clover.core.matrix.grid_oracle_database_manager import get_db
from clover.apps.fridge.app.ports.input.inventory_use_case import InventoryUseCase
from clover.apps.fridge.app.use_cases.inventory_interactor import InventoryInteractor


def get_inventory_repository(
        db: AsyncSession = Depends(get_db)
) -> InventoryPgRepository:
        return InventoryPgRepository(session=db)

def get_inventory_use_case(
        repository: InventoryRepository = Depends(get_inventory_repository)
) -> InventoryUseCase:
        return InventoryInteractor(repository=repository)
