from typing import Protocol

from core.query_helpers import order_by_sql

from .repository import (
    create_customer,
    get_all_customers,
    get_customer_by_id,
    update_customer,
    delete_customer,
)


class ICustomerService(Protocol):
    def get_all(self, sort_by: str, sort_dir: str) -> list: ...
    def create(self, data: dict) -> None: ...
    def get_by_id(self, id: int) -> dict | None: ...
    def update(self, id: int, data: dict) -> None: ...


class CustomerService:
    def get_all(self, sort_by: str, sort_dir: str) -> list:
        return get_all_customers(order_by_sql(sort_by, sort_dir))

    def create(self, data: dict) -> None:
        create_customer(
            data["cust_surname"],
            data["cust_name"],
            data.get("cust_patronymic"),
            data["phone_number"],
            data.get("city"),
            data.get("street"),
            data.get("zip_code"),
            data["percent"],
        )

    def get_by_id(self, id: int) -> dict | None:
        return get_customer_by_id(id)

    def update(self, id: int, data: dict) -> None:
        return update_customer(id, data)

    def delete(self, customer_id: int) -> None:
        delete_customer(customer_id)
