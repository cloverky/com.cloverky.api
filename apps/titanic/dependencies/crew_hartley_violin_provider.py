from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from titanic.adapter.outbound.pg.crew_hartley_violin_pg_repository import HartleyViolinPgRepository
from titanic.app.ports.output.crew_hartley_violin_repository import HartleyViolinRepository
from clover.core.matrix.grid_oracle_database_manager import get_db
from titanic.app.ports.input.crew_hartley_violin_use_case import HartleyViolinUseCase
from titanic.app.use_cases.crew_hartley_violin_interactor import HartleyViolinInteractor

def get_hartley_violin_repository(
        db: AsyncSession = Depends(get_db)
) -> HartleyViolinPgRepository:
        return HartleyViolinPgRepository(session=db)

def get_hartley_violin_use_case(
        repository: HartleyViolinRepository = Depends(get_hartley_violin_repository)
) -> HartleyViolinUseCase:
        return HartleyViolinInteractor(repository=repository)
