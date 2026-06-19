from __future__ import annotations

from abc import ABC, abstractmethod

from clover.apps.silicon_valley.app.dtos.piper_gilfoyle_sys_dto import GilfoyleSysQuery, GilfoyleSysResponse


class GilfoyleSysPort(ABC):

    @abstractmethod
    def introduce_myself(self, query: GilfoyleSysQuery) -> GilfoyleSysResponse:
        '''길포일의 자기 소개 레포지토리 추상 메소드'''
        pass
