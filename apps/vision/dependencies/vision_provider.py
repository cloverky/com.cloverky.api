from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from clover.core.matrix.grid_oracle_database_manager import get_db
from vision.adapter.outbound.repositories.vision_repository import VisionPgRepository
from vision.app.ports.input.vision_use_case import VisionUseCase
from vision.app.ports.output.vision_port import VisionPort
from vision.app.use_cases.vision_interactor import VisionInteractor


def get_vision_repository(
    db: AsyncSession = Depends(get_db),
) -> VisionPort:
    return VisionPgRepository(session=db)


def get_vision_use_case(
    repository: VisionPort = Depends(get_vision_repository),
) -> VisionUseCase:
    return VisionInteractor(repository=repository)
