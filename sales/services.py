from decimal import Decimal
from typing import Protocol

from core.repository import get_user_by_id
from sales.repository import (
    add_sale_to_check,
    create_check,
    delete_check_by_id,
    get_all_checks,
    get_check_by_id,
    get_check_items,
    update_check_totals,
    get_total_units_sold,
)


class ICheckService(Protocol):
    def get_all(self, date_from=None, date_to=None, employee_id=None) -> list: ...
    def get_items(self, check_id: int) -> list: ...
    def get_by_id(self, check_id: int) -> dict | None: ...


class CheckService:
    def get_all(self, date_from=None, date_to=None, employee_id=None) -> list:
        clauses, params = [], []
        if date_from:
            clauses.append("c.print_date >= %s")
            params.append(date_from)
        if date_to:
            clauses.append("c.print_date <= %s")
            params.append(date_to)
        if employee_id:
            clauses.append("c.employee_id = %s")
            params.append(employee_id)
        where_sql = (" WHERE " + " AND ".join(clauses)) if clauses else ""
        return get_all_checks(where_sql, params)

    def get_items(self, check_id: int) -> list:
        return get_check_items(check_id)

    def get_by_id(self, check_id: int) -> dict | None:
        return get_check_by_id(check_id)

    def delete_check(self, check_id: str):
        delete_check_by_id(check_id)

    def start_check(self, user_id: int, card_id=None) -> int:
        employee_id = get_user_by_id(user_id)["employee_id"]
        return create_check(employee_id, card_id)

    def add_item(
        self, check_id: int, upc: str, product_number: int, selling_price
    ) -> None:
        add_sale_to_check(check_id, upc, product_number, selling_price)

    def finalize_check(self, check_id: int, items: list) -> None:
        sum_total = sum(
            Decimal(str(item["selling_price"])) * item["product_number"]
            for item in items
        )
        vat = (sum_total * Decimal("0.2")).quantize(Decimal("0.0001"))
        update_check_totals(check_id, sum_total, vat)

    def get_total_units_sold(self, product_id: int, date_from: str, date_to: str) -> int:
        result = get_total_units_sold(product_id, date_from, date_to)
        return result["total_units"] or 0 if result else 0
