from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from titanic.adapter.outbound.pg.passenger_isidor_couple_pg_repository import IsidorCouplePgRepository
from titanic.app.ports.output.passenger_isidor_couple_repository import IsidorCoupleRepository
from clover.core.matrix.grid_oracle_database_manager import get_db
from titanic.app.ports.input.passenger_isidor_couple_use_case import IsidorCoupleUseCase
from titanic.app.use_cases.passenger_isidor_couple_interactor import IsidorCoupleInteractor

def get_isidor_couple_use_case(
        db: AsyncSession = Depends(get_db)
) -> IsidorCoupleUseCase:
    repository: IsidorCoupleRepository = IsidorCouplePgRepository(session=db)
    return IsidorCoupleInteractor(repository=repository)