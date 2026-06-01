from __future__ import annotations

from typing import Any

from titanic.app.ports.input.hartley_violin_use_case import HartleyViolinUseCase


class HartleyViolinInteractor(HartleyViolinUseCase):

    async def get_hartley_violin(self) -> dict[str, Any]:
        return {
            "character": "Wallace Hartley",
            "artifact": "violin",
            "title": "침몰 직전의 바이올린",
            "detail": "밴드마스터가 연주하던 마지막 선율.",
            "available": True,
        }
