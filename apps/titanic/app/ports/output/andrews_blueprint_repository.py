from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class AndrewsBlueprintRepository(ABC):

    @abstractmethod
    async def get_andrews_blueprint(self) -> dict[str, Any]:
        ...
