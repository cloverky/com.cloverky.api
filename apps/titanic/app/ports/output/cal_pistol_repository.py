from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class CalPistolRepository(ABC):

    @abstractmethod
    async def get_cal_pistol(self) -> dict[str, Any]:
        ...
