from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from titanic.adapter.outbound.pg.passenger_ruth_survivor_pg_repository import RuthValidationPgRepository
from titanic.app.ports.output.passenger_ruth_survivor_repository import RuthValidationRepository
from clover.core.matrix.grid_oracle_database_manager import get_db
from titanic.app.ports.input.passenger_ruth_survivor_use_case import RuthValidationUseCase
from titanic.app.use_cases.passenger_ruth_survivor_interactor import RuthValidationInteractor

def get_ruth_validation_use_case(
        db: AsyncSession = Depends(get_db)
) -> RuthValidationUseCase:
    repository: RuthValidationRepository = RuthValidationPgRepository(session=db)
    return RuthValidationInteractor(repository=repository)
