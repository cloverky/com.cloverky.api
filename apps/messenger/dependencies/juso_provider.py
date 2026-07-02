from fastapi import Depends
from messenger.adapter.outbound.repositories.juso_repository import JusoPgRepository
from messenger.app.ports.input.juso_use_case import JusoUseCase
from messenger.app.ports.output.juso_repository_port import JusoRepositoryPort
from messenger.app.use_cases.juso_interactor import JusoInteractor
from sqlalchemy.ext.asyncio import AsyncSession

from clover.core.matrix.grid_oracle_database_manager import get_db


def get_juso_repository(
    db: AsyncSession = Depends(get_db),
) -> JusoRepositoryPort:
    return JusoPgRepository(session=db)


def get_juso_use_case(
    repository: JusoRepositoryPort = Depends(get_juso_repository),
) -> JusoUseCase:
    return JusoInteractor(repository=repository)
