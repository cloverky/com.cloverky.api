from fastapi import Depends
from messenger.adapter.outbound.repositories.telegram_repository import (
    TelegramPgRepository,
)
from messenger.app.ports.input.telegram_use_case import TelegramUseCase
from messenger.app.ports.output.telegram_repository_port import TelegramRepositoryPort
from messenger.app.use_cases.telegram_interactor import TelegramInteractor
from sqlalchemy.ext.asyncio import AsyncSession

from clover.core.matrix.grid_oracle_database_manager import get_db


def get_telegram_repository(
    db: AsyncSession = Depends(get_db),
) -> TelegramRepositoryPort:
    return TelegramPgRepository(session=db)


def get_telegram_use_case(
    repository: TelegramRepositoryPort = Depends(get_telegram_repository),
) -> TelegramUseCase:
    return TelegramInteractor(repository=repository)
