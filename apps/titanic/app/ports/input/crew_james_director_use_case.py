from __future__ import annotations

from abc import ABC, abstractmethod

from clover.apps.titanic.app.dtos.crew_james_director_dto import JamesDirectorResponse
from titanic.adapter.inbound.api.schemas.crew_james_director_schema import (
    JamesDirectorSchema,
)


class JamesDirectorUseCase(ABC):
    @abstractmethod
    async def introduce_myself(
        self, schema: JamesDirectorSchema
    ) -> JamesDirectorResponse:
        """제임스 감독의 자기소개 메소드"""
        pass

    @abstractmethod
    async def upload_titanic_file(self, schema: list[JamesDirectorSchema]):
        """제임스 감독의 파일업로드 메소드"""
        pass
