from __future__ import annotations

from titanic.adapter.inbound.api.schemas.passenger_rose_model_schemas import (
    RoseModelSchema,
)
from titanic.app.dtos.passenger_rose_model_dto import (
    PassengerPredictionCommand,
    RoseModelQuery,
    RoseModelResponse,
    SurvivalPredictionResult,
)
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.app.ports.output.passenger_rose_model_port import RoseModelPort
from titanic.app.use_cases._ml_strategy import STRATEGY_REGISTRY


class RoseModelInteractor(RoseModelUseCase):
    def __init__(self, repository: RoseModelPort):
        self.repository = repository

    async def introduce_myself(self, schema: RoseModelSchema) -> RoseModelResponse:
        return await self.repository.introduce_myself(
            RoseModelQuery(
                id=schema.id,
                name=schema.name,
            )
        )

    async def predict_survival(
        self,
        command: PassengerPredictionCommand,
        algorithm: str,
    ) -> SurvivalPredictionResult:
        strategy = STRATEGY_REGISTRY.get(algorithm.lower())
        if strategy is None:
            available = ", ".join(STRATEGY_REGISTRY.keys())
            raise ValueError(
                f"알 수 없는 알고리즘 '{algorithm}'. 사용 가능: {available}"
            )
        return strategy.predict(command)
