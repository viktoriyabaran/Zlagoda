from decimal import Decimal
from typing import Protocol

from django.db import transaction
from django.http import HttpRequest

from core.query_helpers import order_by_sql, resolve_filters
from products.repository import (
    PRODUCT_FILTERS,
    STORE_PRODUCT_FILTERS,
    count_products_in_category,
    create_category,
    create_product,
    create_store_product,
    delete_category,
    delete_product,
    delete_store_product,
    get_all_categories,
    get_all_products,
    get_all_store_products,
    get_category_by_id,
    get_product_by_id,
    get_store_product_by_upc,
    update_category,
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

    def delete(self, category_id: int) -> None:
        count = count_products_in_category(category_id)
        if count > 0:
            raise ValueError(f"Cannot delete category: it has {count} product(s).")
        delete_category(category_id)

    def get_by_id(self, category_id: int) -> dict | None:
        return get_category_by_id(category_id)

    def update(self, category_id: int, category_name: str) -> None:
        update_category(category_id, category_name)


class IProductService(Protocol):
    def create(self, data: dict) -> None: ...
    def get_all(self, request: HttpRequest, sort_by: str, sort_dir: str) -> list: ...
    def get_by_id(self, product_id: int) -> dict | None: ...
    def update(self, product_id: int, data: dict) -> None: ...


class ProductService:
    def get_all(self, request: HttpRequest, sort_by: str, sort_dir: str) -> list:
        _, where_sql, where_params = resolve_filters(request, PRODUCT_FILTERS)
        return get_all_products(
            where_sql, where_params, order_by_sql(sort_by, sort_dir)
        )

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

    def delete(self, product_id: int) -> None:
        delete_product(product_id)


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

    def delete(self, upc: str) -> None:
        delete_store_product(upc)


class IStoreProductListService(Protocol):
    def get_all(
        self, request: HttpRequest, sort_by: str, sort_dir: str
    ) -> list: ...


class StoreProductListService:
    def get_all(
        self, request: HttpRequest, sort_by: str, sort_dir: str
    ) -> list:
        _, where_sql, where_params = resolve_filters(request, STORE_PRODUCT_FILTERS)
        return get_all_store_products(
            where_sql=where_sql,
            where_params=where_params,
            order_by=order_by_sql(sort_by, sort_dir),
        )
