from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fridge.models.receipt import FridgeReceipt, FridgeReceiptLine


class ReceiptRepository:
    async def create_receipt(
        self,
        db: AsyncSession,
        *,
        user_id: int,
        store_name: str | None,
        purchased_date,
        status: str = "parsed",
    ) -> FridgeReceipt:
        row = FridgeReceipt(
            user_id=user_id,
            store_name=store_name,
            purchased_date=purchased_date,
            status=status,
        )
        db.add(row)
        await db.flush()
        return row

    async def create_line(
        self,
        db: AsyncSession,
        *,
        receipt_id: int,
        line_name: str,
        quantity: int,
        unit: str,
        food_id: int | None = None,
        inventory_id: int | None = None,
        raw_text: str | None = None,
    ) -> FridgeReceiptLine:
        row = FridgeReceiptLine(
            receipt_id=receipt_id,
            line_name=line_name.strip(),
            quantity=quantity,
            unit=unit.strip() or "개",
            food_id=food_id,
            inventory_id=inventory_id,
            raw_text=raw_text,
        )
        db.add(row)
        await db.flush()
        return row

    async def list_lines(self, db: AsyncSession, receipt_id: int) -> list[FridgeReceiptLine]:
        r = await db.execute(
            select(FridgeReceiptLine)
            .where(FridgeReceiptLine.receipt_id == receipt_id)
            .order_by(FridgeReceiptLine.id),
        )
        return list(r.scalars().all())
