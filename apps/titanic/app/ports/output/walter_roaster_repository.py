from abc import ABC, abstractmethod
from titanic.app.dtos.walter_roaster_dto import WalterRoasterQuery

class WalterRoasterRepository(ABC):
    '''월터의 승객 명단 관리 저장소'''


    @abstractmethod
    def introduce_myself(self, query: WalterRoasterQuery):
        ''' 승객 명단을 가져오는 메소드'''
        pass