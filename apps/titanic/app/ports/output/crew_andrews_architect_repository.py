from __future__ import annotations

from abc import ABC, abstractmethod

from clover.apps.titanic.app.dtos.crew_andrews_architect_dto import AndrewsArchitectQuery, AndrewsArchitectResponse


class AndrewsArchitectRepository(ABC):
    
    @abstractmethod
    def introduce_myself(self, query: AndrewsArchitectQuery) -> AndrewsArchitectResponse:
        '''앤드류 설계자의 자기 소개 레포지토리 추상 메소드'''
        pass
    