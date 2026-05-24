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
    get_all_store_products,
    get_product_by_id,
    get_store_product_by_upc,
    update_product,
    update_store_product,
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
        promo_price = (data["selling_price"] * PROMO_DISCOUNT).quantize(
            Decimal("0.0001")
        )
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
    def get_by_id(self, product_id: int) -> dict | None: ...
    def update(self, product_id: int, data: dict) -> None: ...


class ProductService:
    def get_all(self, sort_by: str, sort_dir: str) -> list:
        return get_all_products(order_by_sql(sort_by, sort_dir))

    def create(self, data: dict) -> None:
        with transaction.atomic():
            product_id = create_product(data)
            if data.get("add_store_product"):
                _create_store_product_with_optional_promo(
                    {**data, "product": product_id}
                )

    def get_by_id(self, product_id: int) -> dict | None:
        return get_product_by_id(product_id)

    def update(self, product_id: int, data: dict) -> None:
        update_product(product_id, data)


class IStoreProductService(Protocol):
    def create(self, data: dict) -> None: ...


class StoreProductService:
    def create(self, data: dict) -> None:
        with transaction.atomic():
            _create_store_product_with_optional_promo(data)

    def get_by_upc(self, upc: str) -> dict | None:
        return get_store_product_by_upc(upc)

    def update(self, upc: str, data: dict) -> None:
        update_store_product(upc, data)


class IStoreProductListService(Protocol):
    def get_all(self, sort_by: str, sort_dir: str) -> list: ...


class StoreProductListService:
    def get_all(self, sort_by: str, sort_dir: str) -> list:
        return get_all_store_products(order_by=order_by_sql(sort_by, sort_dir))
