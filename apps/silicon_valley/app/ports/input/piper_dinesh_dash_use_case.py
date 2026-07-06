from __future__ import annotations

from abc import ABC, abstractmethod

from silicon_valley.adapter.inbound.api.schemas.piper_dinesh_dash_schema import (
    DineshDashSchema,
)

from clover.apps.silicon_valley.app.dtos.piper_dinesh_dash_dto import DineshDashResponse


class DineshDashUseCase(ABC):
    @abstractmethod
    def introduce_myself(self, schema: DineshDashSchema) -> DineshDashResponse:
        """디네쉬의 자기소개 메소드"""
        pass
