from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from titanic.adapter.outbound.pg.passenger_rose_model_pg_repository import RoseModelPgRepository
from titanic.app.ports.output.passenger_rose_model_repository import RoseModelRepository
from clover.core.matrix.grid_oracle_database_manager import get_db
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.app.use_cases.passenger_rose_model_interactor import RoseModelInteractor

def get_rose_model_use_case(
        db: AsyncSession = Depends(get_db)
) -> RoseModelUseCase:
    repository: RoseModelRepository = RoseModelPgRepository(session=db)
    return RoseModelInteractor(repository=repository)