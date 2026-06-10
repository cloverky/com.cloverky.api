from dataclasses import dataclass
from datetime import date


@dataclass
class InventoryItemDto:
    id: int
    food_id: int
    name: str
    quantity: int
    unit: str
    expiry_date: date | None
    purchased_date: date | None
    expiry_is_estimated: bool
    storage: str
    min_quantity: int = 1


@dataclass
class CreateInventoryCommand:
    user_id: int
    name: str
    quantity: int
    unit: str
    expiry_date: date | None
    purchased_date: date | None
    expiry_is_estimated: bool
    storage: str
    min_quantity: int = 1


@dataclass
class UpdateInventoryCommand:
    name: str | None = None
    quantity: int | None = None
    unit: str | None = None
    expiry_date: date | None = None
    storage: str | None = None
    min_quantity: int | None = None


@dataclass
class InventoryStatsDto:
    total: int
    expiring_soon: int
    low_stock: int


@dataclass
class InventoryListDto:
    items: list[InventoryItemDto]
    stats: InventoryStatsDto


@dataclass
class ExpiryEstimateDto:
    name: str
    purchased_date: date
    storage: str
    shelf_life_days: int
    estimated_expiry_date: date
    message: str


@dataclass
class AdjustInventoryResultDto:
    item: InventoryItemDto | None
    removed: bool
    message: str
