from typing import Protocol
from products.repository import get_all_categories, create_category


class ICategoryService(Protocol):
    def get_all(self) -> list: ...
    def create(self, category_name: str) -> None: ...

class CategoryService:
    def get_all(self) -> list:
        return get_all_categories()

    def create(self, category_name: str) -> None:
        create_category(category_name)
