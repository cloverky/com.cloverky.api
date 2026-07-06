from __future__ import annotations

from abc import ABC

from titanic.app.dtos.passenger_rose_model_dto import RoseModelQuery, RoseModelResponse


class RoseModelPort(ABC):
    def introduce_myself(self, query: RoseModelQuery) -> RoseModelResponse:
        raise NotImplementedError
