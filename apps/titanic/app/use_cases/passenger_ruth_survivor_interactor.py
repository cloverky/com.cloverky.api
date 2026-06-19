from __future__ import annotations

from titanic.adapter.inbound.api.schemas.passenger_ruth_validation_schema import RuthValidationSchema
from titanic.app.dtos.passenger_ruth_survivor_dto import RuthValidationQuery, RuthValidationResponse
from titanic.app.ports.input.passenger_ruth_survivor_use_case import RuthValidationUseCase
from titanic.app.ports.output.passenger_ruth_survivor_port import RuthValidationPort


class RuthValidationInteractor(RuthValidationUseCase):

    def __init__(self, repository: RuthValidationPort):
        self.repository = repository

    async def introduce_myself(self, schema: RuthValidationSchema) -> RuthValidationResponse:
        return await self.repository.introduce_myself(RuthValidationQuery(
            id=schema.id,
            name=schema.name
        ))
