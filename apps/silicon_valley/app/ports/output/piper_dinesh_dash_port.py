from __future__ import annotations

from abc import ABC, abstractmethod

from clover.apps.silicon_valley.app.dtos.piper_dinesh_dash_dto import DineshDashQuery, DineshDashResponse


class DineshDashPort(ABC):

    @abstractmethod
    def introduce_myself(self, query: DineshDashQuery) -> DineshDashResponse:
        '''디네쉬의 자기 소개 레포지토리 추상 메소드'''
        pass
