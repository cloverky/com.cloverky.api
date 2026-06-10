from abc import ABC, abstractmethod
from titanic.adapter.inbound.api.schemas.crew_walter_roaster_schema import WalterRoasterSchema
from clover.apps.titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterResponse

class WalterRoasterUseCase(ABC):

    @abstractmethod
    def introduce_myself(self, schema: WalterRoasterSchema) -> WalterRoasterResponse:
        '''월터의 자기소개 메소드'''
        pass