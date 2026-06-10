from fridge.adapter.inbound.api.schemas.inventory_schemas import (
    InventoryAdjustResponse,
    InventoryExpiryEstimateResponse,
    InventoryItemResponse,
    InventoryListResponse,
    InventoryStatsResponse,
)
from fridge.adapter.inbound.api.schemas.receipt_schemas import ReceiptLineResponse, ReceiptScanResponse
from fridge.app.use_cases._shelf_life import (
    InventoryStatusItem,
    compute_status,
    format_quantity,
    shelf_life_hint,
)
from fridge.app.dtos.inventory_dto import (
    AdjustInventoryResultDto,
    ExpiryEstimateDto,
    InventoryItemDto,
    InventoryListDto,
)
from fridge.app.dtos.receipt_dto import ReceiptScanResultDto


def to_inventory_item_response(item: InventoryItemDto) -> InventoryItemResponse:
    status_item = InventoryStatusItem(
        name=item.name,
        quantity=item.quantity,
        unit=item.unit,
        expiry_date=item.expiry_date,
        purchased_date=item.purchased_date,
        expiry_is_estimated=item.expiry_is_estimated,
        storage=item.storage,
        min_quantity=item.min_quantity,
    )
    return InventoryItemResponse(
        id=item.id,
        name=item.name,
        quantity=item.quantity,
        unit=item.unit,
        quantity_label=format_quantity(item.quantity, item.unit),
        expiry_date=item.expiry_date,
        purchased_date=item.purchased_date,
        expiry_is_estimated=item.expiry_is_estimated,
        shelf_life_days=shelf_life_hint(status_item),
        storage=item.storage,
        min_quantity=item.min_quantity,
        status=compute_status(status_item),
    )


def to_inventory_list_response(dto: InventoryListDto) -> InventoryListResponse:
    return InventoryListResponse(
        items=[to_inventory_item_response(i) for i in dto.items],
        stats=InventoryStatsResponse(
            total=dto.stats.total,
            expiring_soon=dto.stats.expiring_soon,
            low_stock=dto.stats.low_stock,
        ),
    )


def to_expiry_estimate_response(dto: ExpiryEstimateDto) -> InventoryExpiryEstimateResponse:
    return InventoryExpiryEstimateResponse(
        name=dto.name,
        purchased_date=dto.purchased_date,
        storage=dto.storage,
        shelf_life_days=dto.shelf_life_days,
        estimated_expiry_date=dto.estimated_expiry_date,
        message=dto.message,
    )


def to_adjust_response(dto: AdjustInventoryResultDto) -> InventoryAdjustResponse:
    return InventoryAdjustResponse(
        item=to_inventory_item_response(dto.item) if dto.item else None,
        removed=dto.removed,
        message=dto.message,
    )


def to_receipt_scan_response(dto: ReceiptScanResultDto) -> ReceiptScanResponse:
    return ReceiptScanResponse(
        receipt_id=dto.receipt_id,
        store_name=dto.store_name,
        purchased_date=dto.purchased_date,
        status=dto.status,
        lines=[
            ReceiptLineResponse(
                id=line.id,
                line_name=line.line_name,
                quantity=line.quantity,
                unit=line.unit,
                food_id=line.food_id,
                inventory_id=line.inventory_id,
            )
            for line in dto.lines
        ],
        inventory_created=dto.inventory_created,
    )
