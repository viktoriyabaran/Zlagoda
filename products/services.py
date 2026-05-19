from typing import Protocol

from products.repository import create_category, create_product, get_all_categories


class ICategoryService(Protocol):
    def get_all(self) -> list: ...
    def create(self, category_name: str) -> None: ...


class CategoryService:
    def get_all(self) -> list:
        return get_all_categories()

    def create(self, category_name: str) -> None:
        create_category(category_name)


class IProductService(Protocol):
    def create(self, data: dict) -> None: ...


class ProductService:
    def create(self, data: dict) -> None:
        create_product(data)
