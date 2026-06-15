from dataclasses import dataclass


@dataclass(frozen=True)
class InventoryQuery:
    user_id: int
    food_id: int


@dataclass(frozen=True)
class InventoryExpiryResponse:
    id: int
    food_id: int
