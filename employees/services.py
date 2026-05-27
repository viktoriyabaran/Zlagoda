from typing import Protocol

from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.http import HttpRequest

from core.query_helpers import order_by_sql, resolve_filters
from core.repository import create_user
from employees.repository import (
    EMPLOYEE_FILTERS,
    create_employee,
    delete_employee,
    get_all_employees,
    get_employee_by_id,
    update_employee,
)


class IEmployeeService(Protocol):
    def create_employee(self, data: dict) -> None: ...
    def get_all(self, request: HttpRequest, sort_by: str, sort_dir: str) -> list: ...
    def get_by_id(self, employee_id: int) -> dict | None: ...
    def update_employee(self, employee_id: int, data: dict) -> None: ...


class EmployeeService:
    def get_all(self, request: HttpRequest, sort_by: str, sort_dir: str) -> list:
        _, where_sql, where_params = resolve_filters(request, EMPLOYEE_FILTERS)
        return get_all_employees(
            where_sql, where_params, order_by_sql(sort_by, sort_dir)
        )

    def get_by_id(self, employee_id: int) -> dict | None:
        return get_employee_by_id(employee_id)

    def create_employee(self, data: dict) -> None:
        with transaction.atomic():
            employee_id = create_employee(data)
            if data.get("has_user_account"):
                create_user(
                    data["username"],
                    make_password(data["password"]),
                    employee_id,
                )

    def update_employee(self, employee_id: int, data: dict) -> None:
        update_employee(employee_id, data)

    def delete(self, employee_id: int) -> None:
        delete_employee(employee_id)
