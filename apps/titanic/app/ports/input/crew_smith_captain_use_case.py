from __future__ import annotations
from abc import ABC, abstractmethod
from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import SmithCaptainSchema
from clover.apps.titanic.app.dtos.crew_smith_captain_dto import SmithCaptainResponse

class SmithCaptainUseCase(ABC):

    @abstractmethod
    def introduce_myself(self, schema: SmithCaptainSchema) -> SmithCaptainResponse:
        '''스미스 선장의 자기소개 메소드'''
        pass