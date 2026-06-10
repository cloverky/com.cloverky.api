from __future__ import annotations

from titanic.adapter.inbound.api.schemas.passenger_isidor_couple_schema import IsidorCoupleSchema
from clover.apps.titanic.app.dtos.passenger_isidor_couple_dto import IsidorCoupleQuery, IsidorCoupleResponse
from clover.apps.titanic.app.ports.input.passenger_isidor_couple_use_case import IsidorCoupleUseCase
from clover.apps.titanic.app.ports.output.passenger_isidor_couple_repository import IsidorCoupleRepository


class IsidorCoupleInteractor(IsidorCoupleUseCase):

    def __init__(self, repository: IsidorCoupleRepository):
        self.repository = repository

    async def introduce_myself(self, schema: IsidorCoupleSchema) -> IsidorCoupleResponse:
        '''이시도어 커플의 자기소개 인터렉트'''

        return await self.repository.introduce_myself(IsidorCoupleQuery(
            id=schema.id,
            name=schema.name
        ))
