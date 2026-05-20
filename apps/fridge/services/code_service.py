from sqlalchemy.ext.asyncio import AsyncSession

from fridge.models.code_model import FridgeCode
from fridge.repositories.code_repository import CodeRepository
from fridge.schemas.code_schema import CodeCreate


class CodeService:
    def __init__(self) -> None:
        self._repo = CodeRepository()

    async def resolve_code(self, db: AsyncSession, code: str) -> FridgeCode | None:
        return await self._repo.get_by_code(db, code)

    async def list_codes_for_food(self, db: AsyncSession, food_id: int) -> list[FridgeCode]:
        return await self._repo.list_by_food(db, food_id)

    async def register_code(self, db: AsyncSession, data: CodeCreate) -> FridgeCode:
        return await self._repo.create(db, data)
