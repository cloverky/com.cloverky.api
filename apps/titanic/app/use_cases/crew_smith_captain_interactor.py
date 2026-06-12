from __future__ import annotations

from fastapi.params import Depends

from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import ChatSchema, SmithCaptainSchema
from titanic.app.dtos.crew_smith_captain_dto import SmithCaptainQuery, SmithCaptainResponse
from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.app.ports.output.crew_smith_captain_repository import SmithCaptainRepository
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.dependencies.passenger_jack_trainer_provider import get_jack_train_use_case
from titanic.dependencies.passenger_rose_model_provider import get_rose_model_use_case



class SmithCaptainInteractor(SmithCaptainUseCase):

    def __init__(self, repository: SmithCaptainRepository):
        self.repository = repository

    async def chat(self, schema: ChatSchema,
                   jack: JackTrainerUseCase = Depends(get_jack_train_use_case),
                   rose: RoseModelUseCase = Depends(get_rose_model_use_case)
                   ) -> SmithCaptainResponse:



        return await self.repository.chat(schema.message)

    async def introduce_myself(self, schema: SmithCaptainSchema) -> SmithCaptainResponse:
        '''스미스 선장의 자기소개 인터렉트'''

        return await self.repository.introduce_myself(SmithCaptainQuery(
            id=schema.id,
            name=schema.name
        ))
