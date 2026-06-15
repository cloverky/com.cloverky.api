from dataclasses import dataclass


@dataclass(frozen=True)
class CategoryQuery:
    name: str


@dataclass(frozen=True)
class CategoryResponse:
    id: int
    name: str
