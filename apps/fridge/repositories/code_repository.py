from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fridge.models.code_model import FridgeCode
from fridge.schemas.code_schema import CodeCreate


class CodeRepository:
    async def get_by_code(self, db: AsyncSession, code: str) -> FridgeCode | None:
        key = code.strip()
        r = await db.execute(select(FridgeCode).where(FridgeCode.code == key).limit(1))
        return r.scalar_one_or_none()

    async def list_by_food(self, db: AsyncSession, food_id: int) -> list[FridgeCode]:
        r = await db.execute(select(FridgeCode).where(FridgeCode.food_id == food_id))
        return list(r.scalars().all())

    async def create(self, db: AsyncSession, data: CodeCreate) -> FridgeCode:
        row = FridgeCode(
            food_id=data.food_id,
            code=data.code.strip(),
            code_type=data.code_type.strip() or "barcode",
        )
        db.add(row)
        await db.commit()
        await db.refresh(row)
        return row
