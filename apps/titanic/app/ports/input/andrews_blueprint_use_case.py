from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class AndrewsBlueprintUseCase(ABC):

    @abstractmethod
    async def get_andrews_blueprint(self) -> dict[str, Any]:
        pass
