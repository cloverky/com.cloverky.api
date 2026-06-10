from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from titanic.adapter.outbound.pg.passenger_molly_scaler_pg_repository import MollyScalerPgRepository
from titanic.app.ports.output.passenger_molly_scaler_repository import MollyScalerRepository
from clover.core.matrix.grid_oracle_database_manager import get_db
from titanic.app.ports.input.passenger_molly_scaler_use_case import MollyScalerUseCase
from titanic.app.use_cases.passenger_molly_scaler_interactor import MollyScalerInteractor

def get_molly_scaler_use_case(
        db: AsyncSession = Depends(get_db)
) -> MollyScalerUseCase:
    repository: MollyScalerRepository = MollyScalerPgRepository(session=db)
    return MollyScalerInteractor(repository=repository)