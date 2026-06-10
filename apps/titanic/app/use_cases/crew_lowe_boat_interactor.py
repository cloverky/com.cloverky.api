from __future__ import annotations

from titanic.adapter.inbound.api.schemas.crew_Iowe_boat_schema import LoweBoatSchema
from clover.apps.titanic.app.dtos.crew_lowe_boat_dto import LoweBoatQuery, LoweBoatResponse
from clover.apps.titanic.app.ports.input.crew_lowe_boat_use_case import LoweBoatUseCase
from clover.apps.titanic.app.ports.output.crew_lowe_boat_repository import LoweBoatRepository


class LoweBoatInteractor(LoweBoatUseCase):

    def __init__(self, repository: LoweBoatRepository):
        self.repository = repository

    async def introduce_myself(self, schema: LoweBoatSchema) -> LoweBoatResponse:
        '''로우 보트의 자기소개 인터렉트'''

        return await self.repository.introduce_myself(LoweBoatQuery(
            id=schema.id,
            name=schema.name
        ))
