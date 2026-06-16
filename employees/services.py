from typing import Protocol

from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.http import HttpRequest

from core.query_helpers import order_by_sql, resolve_filters
from core.repository import create_user
from employees.repository import (
    count_checks_for_employee,
    create_employee,
    delete_employee,
    get_all_employees,
    get_check_counts_by_employee,
    get_employee_by_id,
    get_employee_by_user_id,
    update_employee,
)
from employees.table_config import EMPLOYEE_FILTERS


def employee_block_reason(count: int) -> str:
    return (
        f"Cannot delete employee: they are linked to {count} check(s)." if count else ""
    )


class IEmployeeService(Protocol):
    def create_employee(self, data: dict) -> None: ...
    def get_all(self, request: HttpRequest, sort_by: str, sort_dir: str) -> list: ...
    def get_by_id(self, employee_id: int) -> dict | None: ...
    def get_by_user_id(self, user_id: int) -> dict | None: ...
    def update_employee(self, employee_id: int, data: dict) -> None: ...


class EmployeeService:
    def get_all(
        self, request: HttpRequest, sort_by: str | None, sort_dir: str | None
    ) -> list:
        _, where_sql, where_params = resolve_filters(request, EMPLOYEE_FILTERS)
        return get_all_employees(
            where_sql, where_params, order_by_sql(sort_by, sort_dir)
        )

    def get_by_id(self, employee_id: int) -> dict | None:
        return get_employee_by_id(employee_id)

    def get_by_user_id(self, user_id: int) -> dict | None:
        return get_employee_by_user_id(user_id)

    def create_employee(self, data: dict) -> None:
        with transaction.atomic():
            employee_id = create_employee(data)
            if data.get("has_user_account") and employee_id is not None:
                create_user(
                    data["username"],
                    make_password(data["password"]),
                    employee_id,
                )

    def update_employee(self, employee_id: int, data: dict) -> None:
        update_employee(employee_id, data)

    def delete(self, employee_id: int) -> None:
        reason = employee_block_reason(count_checks_for_employee(employee_id))
        if reason:
            raise ValueError(reason)
        delete_employee(employee_id)

    def annotate_deletable(self, rows: list) -> list:
        counts = get_check_counts_by_employee()
        for row in rows:
            row["delete_block_reason"] = employee_block_reason(counts.get(row["id"], 0))
        return rows
