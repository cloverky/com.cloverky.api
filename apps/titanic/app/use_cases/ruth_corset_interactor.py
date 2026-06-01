from __future__ import annotations

from typing import Any

from titanic.app.ports.input.ruth_corset_use_case import RuthCorsetUseCase


class RuthCorsetInteractor(RuthCorsetUseCase):

    async def get_ruth_corset(self) -> dict[str, Any]:
        return {
            "character": "Ruth DeWitt Bukater",
            "artifact": "corset",
            "title": "코르셋 조이기",
            "detail": "로즈의 허리를 조여 신분과 혼인을 강요하던 빅토리아식 코르셋.",
            "available": True,
        }
