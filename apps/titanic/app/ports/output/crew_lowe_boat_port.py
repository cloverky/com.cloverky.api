from __future__ import annotations

from abc import ABC, abstractmethod

from clover.apps.titanic.app.dtos.crew_lowe_boat_dto import LoweBoatQuery, LoweBoatResponse


class LoweBoatPort(ABC):

    @abstractmethod
    def introduce_myself(self, query: LoweBoatQuery) -> LoweBoatResponse:
        '''로우 보트의 자기 소개 레포지토리 추상 메소드'''
        pass
