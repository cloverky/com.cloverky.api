from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from clover.apps.fridge.adapter.outbound.pg.user_pg_repository import UserPgRepository
from clover.apps.fridge.app.ports.input.user_use_case import UserUseCase
from clover.apps.fridge.app.ports.output.user_repository import UserRepository
from clover.apps.fridge.app.use_cases.user_interactor import UserInteractor
from clover.core.matrix.grid_oracle_database_manager import get_db


def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserPgRepository:
    return UserPgRepository(session=db)


def get_user_use_case(
    repository: UserRepository = Depends(get_user_repository),
) -> UserUseCase:
    return UserInteractor(repository=repository)
