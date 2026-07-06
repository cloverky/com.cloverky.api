from abc import ABC, abstractmethod


class JasonMaskRepository(ABC):
    @abstractmethod
    def get_jason_mask(self) -> str:
        pass
