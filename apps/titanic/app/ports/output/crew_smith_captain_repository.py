from __future__ import annotations

from abc import ABC, abstractmethod
from clover.apps.titanic.app.dtos.crew_smith_captain_dto import SmithCaptainQuery, SmithCaptainResponse

class SmithCaptainRepository(ABC):

    @abstractmethod
    def introduce_myself(self, query: SmithCaptainQuery) -> SmithCaptainResponse:
        '''스미스 선장의 자기 소개 레포지토리 추상 메소드'''
        pass
    