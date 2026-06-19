from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from titanic.adapter.outbound.repositories.passenger_cal_tester_repository import CalTesterPgRepository
from titanic.app.ports.output.passenger_cal_tester_port import CalTesterPort
from clover.core.matrix.grid_oracle_database_manager import get_db
from titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from titanic.app.use_cases.passenger_cal_tester_interactor import CalTesterInteractor

def get_cal_tester_repository(
        db: AsyncSession = Depends(get_db)
) -> CalTesterPgRepository:
        return CalTesterPgRepository(session=db)

def get_cal_tester_use_case(
        repository: CalTesterPort = Depends(get_cal_tester_repository)
) -> CalTesterUseCase:
        return CalTesterInteractor(repository=repository)
