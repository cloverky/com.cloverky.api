from fastapi import Depends
from messenger.adapter.outbound.repositories.discord_repository import (
    DiscordPgRepository,
)
from messenger.app.ports.input.discord_use_case import DiscordUseCase
from messenger.app.ports.output.discord_repository_port import DiscordRepositoryPort
from messenger.app.use_cases.discord_interactor import DiscordInteractor
from sqlalchemy.ext.asyncio import AsyncSession

from clover.core.matrix.grid_oracle_database_manager import get_db


def get_discord_repository(
    db: AsyncSession = Depends(get_db),
) -> DiscordRepositoryPort:
    return DiscordPgRepository(session=db)


def get_discord_use_case(
    repository: DiscordRepositoryPort = Depends(get_discord_repository),
) -> DiscordUseCase:
    return DiscordInteractor(repository=repository)
