from abc import ABC , abstractmethod

from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterQuery, WalterRoasterResponse

class WalterRoasterRepository(ABC):
    '''월터의 승객 명단 관리 저장소'''

    @abstractmethod
    def introduce_myself(self, query: WalterRoasterQuery) -> WalterRoasterResponse:
        '''월터의 자기 소개 레포지토리 추상 메소드'''
        pass
    