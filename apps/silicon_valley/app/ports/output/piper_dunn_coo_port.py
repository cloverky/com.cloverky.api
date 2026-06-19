from __future__ import annotations

from abc import ABC, abstractmethod

from clover.apps.silicon_valley.app.dtos.piper_dunn_coo_dto import DunnCooQuery, DunnCooResponse


class DunnCooPort(ABC):

    @abstractmethod
    def introduce_myself(self, query: DunnCooQuery) -> DunnCooResponse:
        '''재러드 던의 자기 소개 레포지토리 추상 메소드'''
        pass
