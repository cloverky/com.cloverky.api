from __future__ import annotations

from typing import Any

from titanic.app.ports.input.isidor_bed_use_case import IsidorBedUseCase


class IsidorBedInteractor(IsidorBedUseCase):

    async def get_isidor_bed(self) -> dict[str, Any]:
        return {
            "character": "Isidor & Ida Straus",
            "artifact": "bed",
            "title": "함께한 마지막 침실",
            "detail": "구명보트를 거절하고 부부가 함께한 순간을 상징.",
            "available": True,
        }
