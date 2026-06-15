from dataclasses import dataclass


@dataclass(frozen=True)
class UserQuery:
    username: str


@dataclass(frozen=True)
class UserResponse:
    id: int
    username: str
