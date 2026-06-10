from __future__ import annotations

from titanic.adapter.inbound.api.schemas.passenger_rose_model_schemas import RoseModelSchema
from clover.apps.titanic.app.dtos.passenger_rose_model_dto import RoseModelQuery, RoseModelResponse
from clover.apps.titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from clover.apps.titanic.app.ports.output.passenger_rose_model_repository import RoseModelRepository


class RoseModelInteractor(RoseModelUseCase):

    def __init__(self, repository: RoseModelRepository):
        self.repository = repository

    async def introduce_myself(self, schema: RoseModelSchema) -> RoseModelResponse:
        return await self.repository.introduce_myself(RoseModelQuery(
            id=schema.id,
            name=schema.name
        ))
