from sqlalchemy.ext.asyncio import AsyncSession

from fridge.app.dtos.receipt_dto import ReceiptLineDto
from fridge.app.ports.output.receipt_repository import ReceiptRepository
from fridge.adapter.outbound.orm.receipt_orm import ReceiptLineOrm, ReceiptOrm


class ReceiptPgRepository(ReceiptRepository):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_receipt(
        self,
        user_id: int,
        store_name: str | None,
        purchased_date,
        status: str,
    ) -> int:
        row = ReceiptOrm(
            user_id=user_id,
            store_name=store_name,
            purchased_date=purchased_date,
            status=status,
        )
        self._session.add(row)
        await self._session.flush()
        return row.id

    async def create_line(
        self,
        receipt_id: int,
        line_name: str,
        quantity: int,
        unit: str,
        food_id: int | None,
        inventory_id: int | None,
    ) -> ReceiptLineDto:
        row = ReceiptLineOrm(
            receipt_id=receipt_id,
            line_name=line_name.strip(),
            quantity=quantity,
            unit=unit.strip() or "개",
            food_id=food_id,
            inventory_id=inventory_id,
        )
        self._session.add(row)
        await self._session.flush()
        return ReceiptLineDto(
            id=row.id,
            line_name=row.line_name,
            quantity=row.quantity,
            unit=row.unit,
            food_id=row.food_id,
            inventory_id=row.inventory_id,
        )

    async def commit(self) -> None:
        await self._session.commit()
