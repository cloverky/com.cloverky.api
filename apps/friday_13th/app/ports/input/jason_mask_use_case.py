from abc import ABC, abstractmethod

class JasonMaskUseCase(ABC):
    @abstractmethod
    def get_jason_mask(self) -> str:
        pass