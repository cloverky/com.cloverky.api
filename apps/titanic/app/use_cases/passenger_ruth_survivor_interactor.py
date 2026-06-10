from __future__ import annotations

from titanic.adapter.inbound.api.schemas.passenger_ruth_validation_schema import RuthValidationSchema
from clover.apps.titanic.app.dtos.passenger_ruth_survivor_dto import RuthValidationQuery, RuthValidationResponse
from clover.apps.titanic.app.ports.input.passenger_ruth_survivor_use_case import RuthValidationUseCase
from clover.apps.titanic.app.ports.output.passenger_ruth_survivor_repository import RuthValidationRepository


class RuthValidationInteractor(RuthValidationUseCase):

    def __init__(self, repository: RuthValidationRepository):
        self.repository = repository

    async def introduce_myself(self, schema: RuthValidationSchema) -> RuthValidationResponse:
        return await self.repository.introduce_myself(RuthValidationQuery(
            id=schema.id,
            name=schema.name
        ))
