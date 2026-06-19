from __future__ import annotations

from abc import ABC, abstractmethod
from titanic.app.dtos.crew_smith_captain_dto import SmithCaptainQuery, SmithCaptainResponse, SmithChatResponse


class SmithCaptainPort(ABC):

    @abstractmethod
    async def introduce_myself(self, query: SmithCaptainQuery) -> SmithCaptainResponse:
        '''스미스 선장의 자기 소개 레포지토리 추상 메소드'''
        pass

    @abstractmethod
    async def chat(self, message: str) -> SmithChatResponse:
        '''사용자 메시지를 받아 채팅 응답을 반환'''
        pass
