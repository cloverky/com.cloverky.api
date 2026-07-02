from fastapi import Depends
from messenger.adapter.outbound.repositories.receive_repository import ReceivePgRepository
from messenger.app.ports.input.receive_use_case import ReceiveUseCase
from messenger.app.ports.output.receive_port import ReceiveRepositoryPort
from messenger.app.use_cases.receive_interactor import ReceiveInteractor
from sqlalchemy.ext.asyncio import AsyncSession

from clover.core.matrix.grid_oracle_database_manager import get_db


def get_receive_repository(
    db: AsyncSession = Depends(get_db),
) -> ReceiveRepositoryPort:
    return ReceivePgRepository(session=db)


def get_receive_use_case(
    repository: ReceiveRepositoryPort = Depends(get_receive_repository),
) -> ReceiveUseCase:
    return ReceiveInteractor(repository=repository)
