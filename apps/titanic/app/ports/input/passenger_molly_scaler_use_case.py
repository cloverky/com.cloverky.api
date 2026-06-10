from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from titanic.app.dtos.passenger_molly_scaler_dto import MollyScalerResponse

if TYPE_CHECKING:
    from titanic.adapter.inbound.api.schemas.passenger_molly_scaler_schema import MollyScalerSchema


class MollyScalerUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: MollyScalerSchema) -> MollyScalerResponse:
        ...