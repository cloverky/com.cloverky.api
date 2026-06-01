from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class JackSketchRepository(ABC):

    @abstractmethod
    async def get_jack_sketch(self) -> dict[str, Any]:
        ...
