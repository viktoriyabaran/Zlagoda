from typing import Protocol

from core.sorting import order_by_sql
from .repository import get_all_customers, create_customer

class ICustomerService(Protocol):
    def get_all(self, sort_by: str, sort_dir: str) -> list: ...
    def create(self, data: dict) -> None: ...


class CustomerService:
    def get_all(self, sort_by: str, sort_dir: str) -> list:
        return get_all_customers(order_by_sql(sort_by, sort_dir))

    def create(self, data: dict) -> None:
        create_customer(
            data["card_number"],
            data["cust_surname"],
            data["cust_name"],
            data.get("cust_patronymic"),
            data["phone_number"],
            data.get("city"),
            data.get("street"),
            data.get("zip_code"),
            data["percent"],
        )
