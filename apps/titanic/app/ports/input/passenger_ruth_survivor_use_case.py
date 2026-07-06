from __future__ import annotations

from abc import ABC, abstractmethod

from clover.apps.titanic.app.dtos.passenger_ruth_survivor_dto import (
    RuthValidationResponse,
)
from titanic.adapter.inbound.api.schemas.passenger_ruth_validation_schema import (
    RuthValidationSchema,
)


class RuthValidationUseCase(ABC):
    @abstractmethod
    async def introduce_myself(
        self, schema: RuthValidationSchema
    ) -> RuthValidationResponse: ...
