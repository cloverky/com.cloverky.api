from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from clover.apps.titanic.adapter.outbound.pg.crew_lowe_boat_pg_repository import LoweBoatPgRepository
from clover.apps.titanic.app.ports.output.crew_lowe_boat_repository import LoweBoatRepository
from clover.core.matrix.grid_oracle_database_manager import get_db
from clover.apps.titanic.app.ports.input.crew_lowe_boat_use_case import LoweBoatUseCase
from clover.apps.titanic.app.use_cases.crew_lowe_boat_interactor import LoweBoatInteractor

def get_lowe_boat_use_case(
        db: AsyncSession = Depends(get_db)
) -> LoweBoatUseCase:
    repository: LoweBoatRepository = LoweBoatPgRepository(session=db)
    return LoweBoatInteractor(repository=repository)
