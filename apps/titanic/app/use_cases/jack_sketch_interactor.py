from __future__ import annotations

from typing import Any

from titanic.app.ports.input.jack_sketch_use_case import JackSketchUseCase


class JackSketchInteractor(JackSketchUseCase):

    async def get_jack_sketch(self) -> dict[str, Any]:
        return {
            "character": "Jack Dawson",
            "artifact": "sketch",
            "title": "Rose의 초상 스케치",
            "detail": "1등급 객실에서 그린 연필 드로잉.",
            "available": True,
        }
