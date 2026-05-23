from decimal import Decimal
from typing import Protocol

from django.db import transaction

from core.sorting import order_by_sql
from products.repository import (
    create_category,
    create_product,
    create_store_product,
    get_all_categories,
    get_all_products,
)

PROMO_DISCOUNT = Decimal("0.8")


def _create_store_product_with_optional_promo(data: dict) -> None:
    create_store_product(
        {
            "UPC": data["upc"],
            "UPC_prom": None,
            "product": data["product"],
            "selling_price": data["selling_price"],
            "products_number": data["products_number"],
            "promotional_product": False,
        }
    )
    if data.get("add_promo_variant"):
        promo_price = (data["selling_price"] * PROMO_DISCOUNT).quantize(Decimal("0.0001"))
        create_store_product(
            {
                "UPC": data["promo_upc"],
                "UPC_prom": data["upc"],
                "product": data["product"],
                "selling_price": promo_price,
                "products_number": data["promo_products_number"],
                "promotional_product": True,
            }
        )


class ICategoryService(Protocol):
    def get_all(self, sort_by: str, sort_dir: str) -> list: ...
    def create(self, category_name: str) -> None: ...


class CategoryService:
    def get_all(self, sort_by: str, sort_dir: str) -> list:
        return get_all_categories(order_by_sql(sort_by, sort_dir))

    def create(self, category_name: str) -> None:
        create_category(category_name)


class IProductService(Protocol):
    def create(self, data: dict) -> None: ...
    def get_all(self, sort_by: str, sort_dir: str) -> list: ...


class ProductService:
    def get_all(self, sort_by: str, sort_dir: str) -> list:
        return get_all_products(order_by_sql(sort_by, sort_dir))

    def create(self, data: dict) -> None:
        with transaction.atomic():
            product_id = create_product(data)
            if data.get("add_store_product"):
                _create_store_product_with_optional_promo({**data, "product": product_id})


class IStoreProductService(Protocol):
    def create(self, data: dict) -> None: ...


class StoreProductService:
    def create(self, data: dict) -> None:
        with transaction.atomic():
            _create_store_product_with_optional_promo(data)
