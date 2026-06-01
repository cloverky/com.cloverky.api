from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class RoseDiamondUseCase(ABC):

    @abstractmethod
    async def get_rose_diamond(self) -> dict[str, Any]:
        pass
