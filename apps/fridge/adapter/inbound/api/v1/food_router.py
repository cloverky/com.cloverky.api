from fastapi import APIRouter, Depends, HTTPException, Query

from fridge.adapter.inbound.api.schemas.food_catalog_schemas import (
    FoodCreateRequest,
    FoodResponse,
)
from fridge.app.dtos.food_catalog_dto import CreateFoodCommand
from fridge.app.ports.input.food_catalog_use_case import FoodCatalogUseCase
from fridge.dependencies.food_catalog import get_food_catalog_use_case

food_router = APIRouter(prefix="/foods", tags=["foods"])


@food_router.get("", response_model=list[FoodResponse])
async def list_foods(
    category_id: int = Query(..., ge=1),
    catalog: FoodCatalogUseCase = Depends(get_food_catalog_use_case),
) -> list[FoodResponse]:
    return [
        FoodResponse(
            id=f.id,
            category_id=f.category_id,
            name=f.name,
            description=f.description,
            default_unit=f.default_unit,
        )
        for f in await catalog.list_foods(category_id)
    ]


@food_router.get("/{food_id}", response_model=FoodResponse)
async def get_food(
    food_id: int,
    catalog: FoodCatalogUseCase = Depends(get_food_catalog_use_case),
) -> FoodResponse:
    food = await catalog.get_food(food_id)
    if food is None:
        raise HTTPException(status_code=404, detail="식품을 찾을 수 없습니다.")
    return FoodResponse(
        id=food.id,
        category_id=food.category_id,
        name=food.name,
        description=food.description,
        default_unit=food.default_unit,
    )


@food_router.post("", response_model=FoodResponse, status_code=201)
async def create_food(
    body: FoodCreateRequest,
    catalog: FoodCatalogUseCase = Depends(get_food_catalog_use_case),
) -> FoodResponse:
    food = await catalog.create_food(
        CreateFoodCommand(
            category_id=body.category_id,
            name=body.name,
            description=body.description,
            default_unit=body.default_unit,
        ),
    )
    return FoodResponse(
        id=food.id,
        category_id=food.category_id,
        name=food.name,
        description=food.description,
        default_unit=food.default_unit,
    )
