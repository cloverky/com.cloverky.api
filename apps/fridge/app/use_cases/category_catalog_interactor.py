from fridge.app.dtos.food_catalog_dto import CategoryDto, CreateCategoryCommand
from fridge.app.ports.input.category_catalog_use_case import CategoryCatalogUseCase
from fridge.app.ports.output.category_repository import CategoryRepository


class CategoryCatalogInteractor(CategoryCatalogUseCase):

    def __init__(self, categories: CategoryRepository) -> None:
        self._categories = categories

    async def list_categories(self) -> list[CategoryDto]:
        return await self._categories.list_all()

    async def create_category(self, command: CreateCategoryCommand) -> CategoryDto:
        category = await self._categories.create_category(command)
        await self._categories.commit()
        return category
