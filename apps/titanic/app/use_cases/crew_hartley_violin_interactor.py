from __future__ import annotations

from titanic.adapter.inbound.api.schemas.crew_hartley_violin_schema import HartleyViolinSchema
from clover.apps.titanic.app.dtos.crew_hartley_violin_dto import HartleyViolinQuery, HartleyViolinResponse
from clover.apps.titanic.app.ports.input.crew_hartley_violin_use_case import HartleyViolinUseCase
from clover.apps.titanic.app.ports.output.crew_hartley_violin_repository import HartleyViolinRepository


class HartleyViolinInteractor(HartleyViolinUseCase):

    def __init__(self, repository: HartleyViolinRepository):
        self.repository = repository

    async def introduce_myself(self, schema: HartleyViolinSchema) -> HartleyViolinResponse:
        '''하틀리 바이올린의 자기소개 인터렉트'''

        return await self.repository.introduce_myself(HartleyViolinQuery(
            id=schema.id,
            name=schema.name
        ))
