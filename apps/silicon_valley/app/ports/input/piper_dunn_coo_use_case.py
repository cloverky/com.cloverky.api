from __future__ import annotations

from abc import ABC, abstractmethod

from silicon_valley.adapter.inbound.api.schemas.piper_dunn_coo_schema import DunnCooSchema
from clover.apps.silicon_valley.app.dtos.piper_dunn_coo_dto import DunnCooResponse


class DunnCooUseCase(ABC):

    @abstractmethod
    def introduce_myself(self, schema: DunnCooSchema) -> DunnCooResponse:
        '''재러드 던의 자기소개 메소드'''
        pass
