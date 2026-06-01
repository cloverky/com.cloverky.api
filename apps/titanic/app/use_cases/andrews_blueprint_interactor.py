from __future__ import annotations

from typing import Any

from titanic.app.ports.input.andrews_blueprint_use_case import AndrewsBlueprintUseCase


class AndrewsBlueprintInteractor(AndrewsBlueprintUseCase):

    async def get_andrews_blueprint(self) -> dict[str, Any]:
        return {
            "character": "Thomas Andrews",
            "artifact": "blueprint",
            "title": "RMS Titanic 설계 도면",
            "detail": "선체·격실·승객 동선을 담은 설계 청사진.",
            "available": True,
        }
