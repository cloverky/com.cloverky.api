from dataclasses import dataclass


@dataclass(frozen=True)
class FoodsQuery:
    category_id: int
    name: str


@dataclass(frozen=True)
class FoodCatalogResponse:
    id: int
    name: str
