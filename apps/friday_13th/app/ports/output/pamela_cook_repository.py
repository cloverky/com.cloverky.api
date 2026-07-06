from abc import ABC, abstractmethod


class PamelaCookRepository(ABC):
    @abstractmethod
    def get_pamela_cook(self) -> str:
        pass
