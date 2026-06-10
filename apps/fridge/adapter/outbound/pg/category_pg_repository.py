from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fridge.adapter.outbound.orm.category_orm import CategoryOrm
from fridge.app.dtos.food_catalog_dto import CategoryDto, CreateCategoryCommand
from fridge.app.ports.output.category_repository import CategoryRepository


class CategoryPgRepository(CategoryRepository):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _to_dto(self, row: CategoryOrm) -> CategoryDto:
        return CategoryDto(id=row.id, name=row.name, sort_order=row.sort_order)

    async def get_or_create_default(self, name: str, sort_order: int = 999) -> int:
        key = name.strip()
        result = await self._session.execute(
            select(CategoryOrm).where(CategoryOrm.name == key).limit(1),
        )
        existing = result.scalar_one_or_none()
        if existing:
            return existing.id
        row = CategoryOrm(name=key, sort_order=sort_order)
        self._session.add(row)
        await self._session.flush()
        await self._session.refresh(row)
        return row.id

    async def list_all(self) -> list[CategoryDto]:
        result = await self._session.execute(
            select(CategoryOrm).order_by(CategoryOrm.sort_order, CategoryOrm.id),
        )
        return [self._to_dto(row) for row in result.scalars().all()]

    async def create_category(self, command: CreateCategoryCommand) -> CategoryDto:
        row = CategoryOrm(name=command.name.strip(), sort_order=command.sort_order)
        self._session.add(row)
        await self._session.flush()
        await self._session.refresh(row)
        return self._to_dto(row)

    async def commit(self) -> None:
        await self._session.commit()
