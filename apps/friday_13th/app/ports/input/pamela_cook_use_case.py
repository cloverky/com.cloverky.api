from abc import ABC, abstractmethod


class PamelaCookUseCase(ABC):
    @abstractmethod
    def get_pamela_cook(self) -> str:
        pass
