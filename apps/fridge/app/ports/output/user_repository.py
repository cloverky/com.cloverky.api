from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class UserDto:
    id: int
    email: str
    default_storage: str


class UserRepository(ABC):

    @abstractmethod
    async def get_by_email(self, email: str) -> UserDto:
        pass
