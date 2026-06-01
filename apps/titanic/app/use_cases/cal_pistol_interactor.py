from __future__ import annotations

from typing import Any

from titanic.app.ports.input.cal_pistol_use_case import CalPistolUseCase


class CalPistolInteractor(CalPistolUseCase):

    async def get_cal_pistol(self) -> dict[str, Any]:
        return {
            "character": "Caledon Hockley",
            "artifact": "pistol",
            "title": "칼의 권총",
            "detail": "선실 추격 장면에 등장한 콜트 리볼버.",
            "available": True,
        }
