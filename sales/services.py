from decimal import Decimal
from typing import Protocol

from core.repository import get_user_by_id
from customers.repository import get_all_customers
from sales.repository import (
    add_sale_to_check,
    create_check,
    delete_check_by_id,
    get_all_checks,
    get_check_by_id,
    get_check_items,
    get_total_units_sold,
)


class ICheckService(Protocol):
    def get_all(self, date_from=None, date_to=None, employee_id=None) -> list: ...
    def get_items(self, check_id: int) -> list: ...
    def get_by_id(self, check_id: int) -> dict | None: ...


class CheckService:
    def get_all(
        self, date_from=None, date_to=None, employee_id=None, check_number=None
    ) -> list:
        clauses, params = [], []
        if date_from:
            clauses.append("CAST(c.print_date AS DATE) >= %s")
            params.append(date_from)
        if date_to:
            clauses.append("CAST(c.print_date AS DATE) <= %s")
            params.append(date_to)
        if employee_id:
            clauses.append("c.employee_id = %s")
            params.append(employee_id)
        if check_number:
            clauses.append("CAST(c.id AS TEXT) ILIKE %s")
            params.append(f"%{check_number}%")
        where_sql = (" WHERE " + " AND ".join(clauses)) if clauses else ""
        return get_all_checks(where_sql, params)

    def get_items(self, check_id: int) -> list:
        return get_check_items(check_id)

    def get_by_id(self, check_id: int) -> dict | None:
        return get_check_by_id(check_id)

    def delete_check(self, check_id: str):
        delete_check_by_id(check_id)

    def start_check(self, user_id: int, card_id=None) -> int:
        user = get_user_by_id(user_id)
        if not user:
            raise ValueError(f"No user found for id {user_id}")
        check_id = create_check(user["employee_id"], card_id)
        if check_id is None:
            raise RuntimeError("Failed to create check")
        return check_id

    def add_item(
        self, check_id: int, upc: str, product_number: int, selling_price
    ) -> None:
        add_sale_to_check(check_id, upc, product_number, selling_price)

    def resolve_discount_percent(self, card_id) -> int:
        clean = str(card_id).strip() if card_id else ""
        if not clean or clean == "None":
            return 0
        card = next((c for c in get_all_customers() if str(c["id"]) == clean), None)
        return int(card["percent"] or 0) if card else 0

    def compute_totals(self, items: list, discount_percent: int) -> dict:
        cents = Decimal("0.0001")
        raw_total = sum(
            (Decimal(str(i["selling_price"])) * i["quantity"] for i in items),
            Decimal("0"),
        ).quantize(cents)
        discount_amount = (
            raw_total * Decimal(discount_percent) / Decimal("100")
        ).quantize(cents)
        sum_total = raw_total - discount_amount
        vat = (sum_total * Decimal("0.2")).quantize(cents)
        return {
            "raw_total": raw_total,
            "discount_percent": discount_percent,
            "discount_amount": discount_amount,
            "sum_total": sum_total,
            "vat": vat,
        }

    def get_total_units_sold(
        self, product_id: int, date_from: str, date_to: str
    ) -> int:
        result = get_total_units_sold(product_id, date_from, date_to)
        return result["total_units"] or 0 if result else 0
