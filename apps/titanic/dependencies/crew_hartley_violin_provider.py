from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from titanic.adapter.outbound.repositories.crew_hartley_violin_repository import HartleyViolinPgRepository
from titanic.app.ports.output.crew_hartley_violin_port import HartleyViolinPort
from clover.core.matrix.grid_oracle_database_manager import get_db
from titanic.app.ports.input.crew_hartley_violin_use_case import HartleyViolinUseCase
from titanic.app.use_cases.crew_hartley_violin_interactor import HartleyViolinInteractor

def get_hartley_violin_repository(
        db: AsyncSession = Depends(get_db)
) -> HartleyViolinPgRepository:
        return HartleyViolinPgRepository(session=db)

def get_hartley_violin_use_case(
        repository: HartleyViolinPort = Depends(get_hartley_violin_repository)
) -> HartleyViolinUseCase:
        return HartleyViolinInteractor(repository=repository)
