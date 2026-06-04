from abc import ABC, abstractmethod

class WalterRoasterRepository(ABC):
    '''월터의 승객 명단 관리 저장소'''


    @abstractmethod
    def introduce_myself(self):
        ''' 승객 명단을 가져오는 메소드'''
        pass