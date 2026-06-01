from __future__ import annotations

from typing import Any

from titanic.app.ports.output.cal_pistol_repository import CalPistolRepository


class CalPistolPgRepository(CalPistolRepository):

    async def get_cal_pistol(self) -> dict[str, Any]:
        return {
            "character": "Caledon Hockley",
            "artifact": "pistol",
            "title": "칼의 권총",
            "detail": "선실 추격 장면에 등장한 콜트 리볼버.",
            "available": True,
        }
