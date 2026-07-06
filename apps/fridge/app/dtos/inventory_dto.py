from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class InventoryQuery:
    user_id: int
    food_id: int


@dataclass(frozen=True)
class InventoryExpiryResponse:
    id: int
    food_id: int


@dataclass
class InventoryItemDto:
    id: int
    name: str
    quantity: int
    unit: str
    quantity_label: str
    expiry_date: str | None
    purchased_date: str | None
    expiry_is_estimated: bool
    shelf_life_days: int | None
    storage: str
    min_quantity: int
    status: str


@dataclass
class InventoryStatsDto:
    total: int
    expiring_soon: int
    low_stock: int


@dataclass
class InventoryListDto:
    items: list[InventoryItemDto] = field(default_factory=list)
    stats: InventoryStatsDto = field(default_factory=lambda: InventoryStatsDto(0, 0, 0))


@dataclass
class CreateInventoryCommand:
    user_email: str
    name: str
    quantity: int
    unit: str
    expiry_date: str | None
    purchased_date: str | None
    storage: str
    min_quantity: int


@dataclass
class AdjustInventoryCommand:
    user_email: str
    item_id: int
    amount: int


@dataclass
class InventoryAdjustResultDto:
    item: InventoryItemDto | None
    removed: bool
    message: str


@dataclass
class ExpiryEstimateDto:
    name: str
    purchased_date: str
    storage: str
    shelf_life_days: int
    estimated_expiry_date: str
    message: str
