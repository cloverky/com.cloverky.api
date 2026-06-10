from __future__ import annotations

from titanic.adapter.inbound.api.schemas.crew_andrews_architect_schema import AndrewsArchitectSchema
from clover.apps.titanic.app.dtos.crew_andrews_architect_dto import AndrewsArchitectQuery, AndrewsArchitectResponse
from clover.apps.titanic.app.ports.input.crew_andrews_architect_use_case import AndrewsArchitectUseCase
from clover.apps.titanic.app.ports.output.crew_andrews_architect_repository import AndrewsArchitectRepository


class AndrewsArchitectInteractor(AndrewsArchitectUseCase):
    
    def __init__(self, repository: AndrewsArchitectRepository):
        self.repository = repository

    async def introduce_myself(self, schema: AndrewsArchitectSchema) -> AndrewsArchitectResponse:
        '''앤드류 설계자의 자기소개 인터렉트'''

        return await self.repository.introduce_myself(AndrewsArchitectQuery(
            id = schema.id,
            name = schema.name
        ))