from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from clover.apps.fridge.app.dtos.category_dto import CategoryQuery, CategoryResponse
from clover.apps.fridge.app.ports.output.category_repository import CategoryRepository

logger = logging.getLogger(__name__)


class CategoryPgRepository(CategoryRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_list(self, query: CategoryQuery) -> CategoryResponse:
        logger.info(f"[CategoryPgRepository] get_list | query={query}")
        return CategoryResponse(
            id=1,
            name=query.name,
        )
