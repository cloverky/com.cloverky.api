from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class JackTrainerUseCase(ABC):

    @abstractmethod
    async def get_model_info(self) -> dict[str, Any]:
        ...

    @abstractmethod
    async def analyze_jack_dawson(self) -> dict[str, Any]:
        ...

    @abstractmethod
    async def predict_survival(self, passenger_data: dict[str, Any]) -> dict[str, Any]:
        ...