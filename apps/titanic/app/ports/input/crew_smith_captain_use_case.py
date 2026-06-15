from __future__ import annotations
from abc import ABC, abstractmethod
from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import SmithCaptainSchema, ChatSchema
from titanic.app.dtos.crew_smith_captain_dto import SmithCaptainResponse, SmithChatResponse
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase

class SmithCaptainUseCase(ABC):

    @abstractmethod
    def introduce_myself(self, schema: SmithCaptainSchema) -> SmithCaptainResponse:
        '''스미스 선장의 자기소개 메소드'''
        pass

    @abstractmethod
    async def chat(self, schema: ChatSchema,
                   jack: JackTrainerUseCase,
                   rose: RoseModelUseCase
                   ) -> SmithChatResponse:
        '''사용자 자연어 입력을 받아 채팅 응답을 반환'''
        pass