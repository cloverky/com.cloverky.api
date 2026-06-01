from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class TitanicQueryRepository(ABC):

    @abstractmethod
    def get_tree(self) -> dict[str, Any]:
        ...

    @abstractmethod
    def get_model(self) -> dict[str, Any]:
        ...
