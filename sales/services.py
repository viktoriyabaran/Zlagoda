from typing import Protocol

from sales.repository import get_all_checks, get_check_items


class ICheckService(Protocol):
    def get_all(self, date_from=None, date_to=None, employee_id=None) -> list: ...
    def get_items(self, check_id: int) -> list: ...


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
            clauses.append("c.eid_employee = %s")
            params.append(employee_id)
        where_sql = (" WHERE " + " AND ".join(clauses)) if clauses else ""
        return get_all_checks(where_sql, params)

    def get_items(self, check_id: int) -> list:
        return get_check_items(check_id)
