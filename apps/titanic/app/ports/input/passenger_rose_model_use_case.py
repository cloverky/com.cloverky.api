from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.adapter.inbound.api.schemas.passenger_rose_model_schemas import RoseModelSchema
from clover.apps.titanic.app.dtos.passenger_rose_model_dto import (
    PassengerPredictionCommand,
    RoseModelResponse,
    SurvivalPredictionResult,
)


class RoseModelUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: RoseModelSchema) -> RoseModelResponse:
        ...

    @abstractmethod
    async def predict_survival(
        self,
        command: PassengerPredictionCommand,
        algorithm: str,
    ) -> SurvivalPredictionResult:
        ...
