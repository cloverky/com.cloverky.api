from dataclasses import dataclass


@dataclass
class CategoryDto:
    id: int
    name: str
    sort_order: int


@dataclass
class CreateCategoryCommand:
    name: str
    sort_order: int = 0


@dataclass
class FoodDto:
    id: int
    category_id: int
    name: str
    description: str | None
    default_unit: str


@dataclass
class CreateFoodCommand:
    category_id: int
    name: str
    description: str | None = None
    default_unit: str = "개"
