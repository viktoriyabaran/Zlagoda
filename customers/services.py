from typing import Protocol
from .repository import get_all_customers, create_customer

class ICustomerService(Protocol):
    def get_all(self) -> list: ...
    def create(self, data: dict) -> None: ...


class CustomerService:
    def get_all(self) -> list:
        return get_all_customers()

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
