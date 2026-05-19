from decimal import Decimal
from typing import Protocol

from django.db import transaction

from products.repository import (
    create_category,
    create_product,
    create_store_product,
    get_all_categories,
)

PROMO_DISCOUNT = Decimal("0.8")


def _create_store_product_with_optional_promo(data: dict) -> None:
    create_store_product(
        {
            "UPC": data["upc"],
            "UPC_prom": None,
            "id_product": data["id_product"],
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
                "id_product": data["id_product"],
                "selling_price": promo_price,
                "products_number": data["promo_products_number"],
                "promotional_product": True,
            }
        )


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
        with transaction.atomic():
            create_product(data)
            if data.get("add_store_product"):
                _create_store_product_with_optional_promo(data)


class IStoreProductService(Protocol):
    def create(self, data: dict) -> None: ...


class StoreProductService:
    def create(self, data: dict) -> None:
        with transaction.atomic():
            _create_store_product_with_optional_promo(data)
