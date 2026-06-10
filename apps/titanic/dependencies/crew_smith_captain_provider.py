from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from titanic.adapter.outbound.pg.crew_smith_captain_pg_repository import SmithCaptainPgRepository
from titanic.app.ports.output.crew_smith_captain_repository import SmithCaptainRepository
from clover.core.matrix.grid_oracle_database_manager import get_db
from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.app.use_cases.crew_smith_captain_interactor import SmithCaptainInteractor

def get_smith_captain_use_case(
        db: AsyncSession = Depends(get_db)
) -> SmithCaptainUseCase:
    repository: SmithCaptainRepository = SmithCaptainPgRepository(session=db)
    return SmithCaptainInteractor(repository=repository)