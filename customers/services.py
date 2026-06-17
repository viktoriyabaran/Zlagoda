from typing import Protocol

from django.http import HttpRequest

from core.query_helpers import order_by_sql, resolve_filters
from core.roles import Role

from .repository import (
    count_checks_for_customer,
    create_customer,
    delete_customer,
    get_all_customers,
    get_check_counts_by_customer,
    get_customer_by_id,
    get_customer_filters,
    update_customer,
)


def customer_block_reason(count: int) -> str:
    return (
        f"Cannot delete customer: their card is used on {count} check(s)."
        if count
        else ""
    )


class ICustomerService(Protocol):
    def get_all(
        self, request: HttpRequest, sort_by: str | None, sort_dir: str | None
    ) -> list: ...
    def create(self, data: dict) -> None: ...
    def get_by_id(self, id: int) -> dict | None: ...
    def update(self, id: int, data: dict) -> None: ...
    def annotate_deletable(self, rows: list) -> list: ...


class CustomerService:
    def get_all(
        self, request: HttpRequest, sort_by: str | None, sort_dir: str | None
    ) -> list:
        is_cashier = request.session.get("user_role") == Role.CASHIER
        _, where_sql, where_params = resolve_filters(
            request, get_customer_filters(is_cashier)
        )
        return get_all_customers(
            where_sql=where_sql,
            where_params=where_params,
            order_by=order_by_sql(sort_by, sort_dir),
        )

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
        reason = customer_block_reason(count_checks_for_customer(customer_id))
        if reason:
            raise ValueError(reason)
        delete_customer(customer_id)

    def annotate_deletable(self, rows: list) -> list:
        counts = get_check_counts_by_customer()
        for row in rows:
            row["delete_block_reason"] = customer_block_reason(counts.get(row["id"], 0))
        return rows
