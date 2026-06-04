
from abc import ABC, abstractmethod


class WalterRoasterUseCase(ABC):

    @abstractmethod
    def introduce_myself(self):
        ''' 월터의 자기소개 메소드'''
        pass