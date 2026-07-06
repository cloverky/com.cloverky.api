from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from clover.core.matrix.grid_oracle_database_manager import get_db
from titanic.adapter.outbound.repositories.crew_walter_roaster_repository import (
    WalterRoasterPgRepository,
)
from titanic.app.ports.input.crew_walter_roaster_use_case import WalterRoasterUseCase
from titanic.app.ports.output.crew_walter_roaster_port import WalterRoasterPort
from titanic.app.use_cases.crew_walter_roaster_interactor import WalterRoasterInteractor


def get_walter_roaster_repository(
    db: AsyncSession = Depends(get_db),
) -> WalterRoasterPgRepository:
    return WalterRoasterPgRepository(session=db)


def get_walter_roaster_use_case(
    repository: WalterRoasterPort = Depends(get_walter_roaster_repository),
) -> WalterRoasterUseCase:
    return WalterRoasterInteractor(repository=repository)
