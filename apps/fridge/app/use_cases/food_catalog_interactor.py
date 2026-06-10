from fridge.app.dtos.food_catalog_dto import CreateFoodCommand, FoodDto
from fridge.app.ports.input.food_catalog_use_case import FoodCatalogUseCase
from fridge.app.ports.output.food_repository import FoodRepository


class FoodCatalogInteractor(FoodCatalogUseCase):

    def __init__(self, foods: FoodRepository) -> None:
        self._foods = foods

    async def get_food(self, food_id: int) -> FoodDto | None:
        return await self._foods.get_by_id(food_id)

    async def list_foods(self, category_id: int) -> list[FoodDto]:
        return await self._foods.list_by_category(category_id)

    async def create_food(self, command: CreateFoodCommand) -> FoodDto:
        food = await self._foods.create_food(command)
        await self._foods.commit()
        return food
