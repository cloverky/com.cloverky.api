from __future__ import annotations

from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import SmithCaptainSchema
from clover.apps.titanic.app.dtos.crew_smith_captain_dto import SmithCaptainQuery, SmithCaptainResponse
from clover.apps.titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from clover.apps.titanic.app.ports.output.crew_smith_captain_repository import SmithCaptainRepository


class SmithCaptainInteractor(SmithCaptainUseCase):

    def __init__(self, repository: SmithCaptainRepository):
        self.repository = repository

    async def introduce_myself(self, schema: SmithCaptainSchema) -> SmithCaptainResponse:
        '''스미스 선장의 자기소개 인터렉트'''

        return await self.repository.introduce_myself(SmithCaptainQuery(
            id=schema.id,
            name=schema.name
        ))
