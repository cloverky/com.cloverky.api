from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.app.dtos.crew_andrews_architect_dto import AndrewsArchitectQuery, AndrewsArchitectResponse


class AndrewsArchitectPort(ABC):

    @abstractmethod
    async def introduce_myself(self, query: AndrewsArchitectQuery) -> AndrewsArchitectResponse:
        '''앤드류 설계자의 자기 소개 추상 메소드'''
        pass
