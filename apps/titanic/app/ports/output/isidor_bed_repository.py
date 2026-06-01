from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class IsidorBedRepository(ABC):

    @abstractmethod
    async def get_isidor_bed(self) -> dict[str, Any]:
        ...
