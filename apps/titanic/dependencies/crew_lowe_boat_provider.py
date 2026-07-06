from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from clover.core.matrix.grid_oracle_database_manager import get_db
from titanic.adapter.outbound.repositories.crew_lowe_boat_pg_repository import (
    LoweBoatPgRepository,
)
from titanic.app.ports.input.crew_lowe_boat_use_case import LoweBoatUseCase
from titanic.app.ports.output.crew_lowe_boat_port import LoweBoatPort
from titanic.app.use_cases.crew_lowe_boat_interactor import LoweBoatInteractor


def get_lowe_boat_repository(
    db: AsyncSession = Depends(get_db),
) -> LoweBoatPgRepository:
    return LoweBoatPgRepository(session=db)


def get_lowe_boat_use_case(
    repository: LoweBoatPort = Depends(get_lowe_boat_repository),
) -> LoweBoatUseCase:
    return LoweBoatInteractor(repository=repository)
