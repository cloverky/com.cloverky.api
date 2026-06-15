from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from titanic.adapter.outbound.pg.crew_andrews_architect_pg_repository import AndrewsArchitectPgRepository
from titanic.app.ports.output.crew_andrews_architect_repository import AndrewsArchitectRepository
from clover.core.matrix.grid_oracle_database_manager import get_db
from titanic.app.ports.input.crew_andrews_architect_use_case import AndrewsArchitectUseCase
from titanic.app.use_cases.crew_andrews_architect_interactor import AndrewsArchitectInteractor

def get_andrews_architect_repository(
        db: AsyncSession = Depends(get_db)
) -> AndrewsArchitectPgRepository:
        return AndrewsArchitectPgRepository(session=db)

def get_andrews_architect_use_case(
        repository: AndrewsArchitectRepository = Depends(get_andrews_architect_repository)
) -> AndrewsArchitectUseCase:
        return AndrewsArchitectInteractor(repository=repository)
