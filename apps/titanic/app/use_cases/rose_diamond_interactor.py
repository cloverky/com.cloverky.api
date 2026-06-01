from __future__ import annotations

from typing import Any

from titanic.app.ports.input.rose_diamond_use_case import RoseDiamondUseCase


class RoseDiamondInteractor(RoseDiamondUseCase):

    async def get_rose_diamond(self) -> dict[str, Any]:
        return {
            "character": "Rose DeWitt Bukater",
            "artifact": "diamond",
            "title": "Heart of the Ocean",
            "detail": "전설의 푸른 다이아몬드 목걸이.",
            "available": True,
        }
