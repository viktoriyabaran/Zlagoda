from typing import Protocol

from django.contrib.auth.hashers import make_password
from django.db import transaction

from core.repository import create_user
from core.sorting import order_by_sql
from employees.repository import create_employee, get_all_employees


class IEmployeeService(Protocol):
    def create_employee(self, data: dict) -> None: ...
    def get_all(self, sort_by: str, sort_dir: str) -> list: ...


class EmployeeService:
    def get_all(self, sort_by: str, sort_dir: str) -> list:
        return get_all_employees(order_by_sql(sort_by, sort_dir))

    def create_employee(self, data: dict) -> None:
        with transaction.atomic():
            create_employee(data)
            if data.get("has_user_account"):
                create_user(
                    data["username"],
                    make_password(data["password"]),
                    data["id_employee"],
                )
