from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class TitanicQueryUseCase(ABC):

    @abstractmethod
    def get_tree(self) -> dict[str, Any]:
        pass

    @abstractmethod
    def get_model(self) -> dict[str, Any]:
        pass
