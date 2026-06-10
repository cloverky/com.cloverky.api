from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from fridge.adapter.outbound.orm.food_orm import FoodOrm
from fridge.app.dtos.food_catalog_dto import CreateFoodCommand, FoodDto
from fridge.app.ports.output.food_repository import FoodRepository


class FoodPgRepository(FoodRepository):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _to_dto(self, row: FoodOrm) -> FoodDto:
        return FoodDto(
            id=row.id,
            category_id=row.category_id,
            name=row.name,
            description=row.description,
            default_unit=row.default_unit,
        )

    async def find_by_name(self, name: str) -> int | None:
        key = name.strip()
        result = await self._session.execute(
            select(FoodOrm).where(func.lower(FoodOrm.name) == key.lower()).limit(1),
        )
        row = result.scalar_one_or_none()
        return row.id if row else None

    async def create(self, category_id: int, name: str, default_unit: str) -> int:
        row = FoodOrm(
            category_id=category_id,
            name=name.strip(),
            default_unit=default_unit.strip() or "개",
        )
        self._session.add(row)
        await self._session.flush()
        await self._session.refresh(row)
        return row.id

    async def get_by_id(self, food_id: int) -> FoodDto | None:
        result = await self._session.execute(
            select(FoodOrm).where(FoodOrm.id == food_id).limit(1),
        )
        row = result.scalar_one_or_none()
        return self._to_dto(row) if row else None

    async def list_by_category(self, category_id: int) -> list[FoodDto]:
        result = await self._session.execute(
            select(FoodOrm)
            .where(FoodOrm.category_id == category_id)
            .order_by(FoodOrm.name),
        )
        return [self._to_dto(row) for row in result.scalars().all()]

    async def create_food(self, command: CreateFoodCommand) -> FoodDto:
        row = FoodOrm(
            category_id=command.category_id,
            name=command.name.strip(),
            description=command.description.strip() if command.description else None,
            default_unit=command.default_unit.strip() or "개",
        )
        self._session.add(row)
        await self._session.flush()
        await self._session.refresh(row)
        return self._to_dto(row)

    async def commit(self) -> None:
        await self._session.commit()
