from typing import Protocol

from django.contrib.auth.hashers import make_password
from django.db import transaction

from core.repository import create_user
from core.sorting import order_by_sql
from employees.repository import (
    EMPLOYEE_FILTERS,
    create_employee,
    get_all_employees,
    resolve_filters,
)


class IEmployeeService(Protocol):
    def create_employee(self, data: dict) -> None: ...
    def get_all(self, request, sort_by: str, sort_dir: str) -> list: ...


class EmployeeService:
    def get_all(self, request, sort_by: str, sort_dir: str) -> list:
        applied, where_sql, where_params = resolve_filters(request, EMPLOYEE_FILTERS)
        return get_all_employees(
            where_sql, where_params, order_by_sql(sort_by, sort_dir)
        )

    def create_employee(self, data: dict) -> None:
        with transaction.atomic():
            employee_id = create_employee(data)
            if data.get("has_user_account"):
                create_user(
                    data["username"],
                    make_password(data["password"]),
                    employee_id,
                )
