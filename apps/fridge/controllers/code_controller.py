import logging

from sqlalchemy.ext.asyncio import AsyncSession

from fridge.models.code_model import FridgeCode
from fridge.schemas.code_schema import CodeCreate
from fridge.services.code_service import CodeService

logger = logging.getLogger(__name__)


class CodeController:
    def __init__(self) -> None:
        self._service = CodeService()

    async def resolve_code(self, db: AsyncSession, code: str) -> FridgeCode | None:
        return await self._service.resolve_code(db, code)

    async def list_codes(self, db: AsyncSession, food_id: int) -> list[FridgeCode]:
        return await self._service.list_codes_for_food(db, food_id)

    async def register_code(self, db: AsyncSession, data: CodeCreate) -> FridgeCode:
        logger.info("[Fridge CodeController] register_code food_id=%s", data.food_id)
        return await self._service.register_code(db, data)
