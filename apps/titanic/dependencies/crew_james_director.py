from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from titanic.adapter.outbound.repositories.crew_james_director_repository import JamesDirectorPgRepository
from titanic.app.ports.output.crew_james_director_port import JamesDirectorPort
from clover.core.matrix.grid_oracle_database_manager import get_db
from titanic.app.ports.input.crew_james_director_use_case import JamesDirectorUseCase
from titanic.app.use_cases.crew_james_director_interactor import JamesDirectorInteractor

def get_james_director_repository(
        db: AsyncSession = Depends(get_db)
) -> JamesDirectorPgRepository:
        return JamesDirectorPgRepository(session=db)

def get_james_director_use_case(
        repository: JamesDirectorPort = Depends(get_james_director_repository)
) -> JamesDirectorUseCase:
        return JamesDirectorInteractor(repository=repository)
