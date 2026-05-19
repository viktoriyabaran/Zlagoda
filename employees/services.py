from typing import Protocol

from django.contrib.auth.hashers import make_password
from django.db import transaction

from core.repository import create_user
from employees.repository import create_employee


class IEmployeeService(Protocol):
    def create_employee(self, data: dict) -> None: ...


class EmployeeService:
    def create_employee(self, data: dict) -> None:
        with transaction.atomic():
            create_employee(data)
            if data.get("has_user_account"):
                create_user(
                    data["username"],
                    make_password(data["password"]),
                    data["id_employee"],
                )
