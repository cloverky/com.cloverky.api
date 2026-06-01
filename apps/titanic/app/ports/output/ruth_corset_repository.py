from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class RuthCorsetRepository(ABC):

    @abstractmethod
    async def get_ruth_corset(self) -> dict[str, Any]:
        ...
