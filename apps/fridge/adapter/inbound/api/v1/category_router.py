from fastapi import APIRouter, Depends

from fridge.adapter.inbound.api.schemas.food_catalog_schemas import (
    CategoryCreateRequest,
    CategoryResponse,
)
from fridge.app.dtos.food_catalog_dto import CreateCategoryCommand
from fridge.app.ports.input.category_catalog_use_case import CategoryCatalogUseCase
from fridge.dependencies.category_catalog import get_category_catalog_use_case

category_router = APIRouter(prefix="/categories", tags=["categories"])


@category_router.get("", response_model=list[CategoryResponse])
async def list_categories(
    catalog: CategoryCatalogUseCase = Depends(get_category_catalog_use_case),
) -> list[CategoryResponse]:
    return [
        CategoryResponse(id=c.id, name=c.name, sort_order=c.sort_order)
        for c in await catalog.list_categories()
    ]


@category_router.post("", response_model=CategoryResponse, status_code=201)
async def create_category(
    body: CategoryCreateRequest,
    catalog: CategoryCatalogUseCase = Depends(get_category_catalog_use_case),
) -> CategoryResponse:
    category = await catalog.create_category(
        CreateCategoryCommand(name=body.name, sort_order=body.sort_order),
    )
    return CategoryResponse(id=category.id, name=category.name, sort_order=category.sort_order)
