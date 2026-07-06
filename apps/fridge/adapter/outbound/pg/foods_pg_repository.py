from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from clover.apps.fridge.app.dtos.foods_dto import FoodCatalogResponse, FoodsQuery
from clover.apps.fridge.app.ports.output.foods_repository import FoodsRepository

logger = logging.getLogger(__name__)


class FoodsPgRepository(FoodsRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_catalog(self, query: FoodsQuery) -> FoodCatalogResponse:
        logger.info(f"[FoodsPgRepository] get_catalog | query={query}")
        return FoodCatalogResponse(
            id=1,
            name=query.name,
        )
