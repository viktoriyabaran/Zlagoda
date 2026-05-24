from core.db import (
    execute_insert_returning,
    execute_query,
    execute_single,
    execute_write,
)

EMPLOYEE_FILTERS = [
    {"key": "q", "label": "Search surname", "type": "search", "column": "empl_surname"},
    {
        "key": "role",
        "label": "Role",
        "type": "select",
        "column": "empl_role",
        "options": [
            {"value": "Cashier", "label": "Cashier"},
            {"value": "Manager", "label": "Manager"},
        ],
    },
]


def resolve_filters(request, filters):
    applied, clauses, params = {}, [], []
    for f in filters:
        raw = (request.GET.get(f["key"]) or "").strip()
        if not raw:
            continue
        if f["type"] == "select":
            if raw not in {o["value"] for o in f["options"]}:
                continue
            clauses.append(f"{f['column']} = %s")
            params.append(raw)
        elif f["type"] == "search":
            clauses.append(f"{f['column']} ILIKE %s")
            params.append(f"%{raw}%")
        applied[f["key"]] = raw
    where_sql = (" WHERE " + " AND ".join(clauses)) if clauses else ""
    return applied, where_sql, params


def get_all_employees(where_sql="", where_params=(), order_by=""):
    return execute_query(
        f"SELECT id, empl_surname, empl_name, empl_patronymic, empl_role, salary, date_of_birth, date_of_start, phone_number, city, street, zip_code FROM employees_employee{where_sql}{order_by}",
        list(where_params),
    )

def create_employee(data: dict) -> int:
    return execute_insert_returning(
        """
        INSERT INTO employees_employee (
            empl_surname, empl_name, empl_patronymic,
            empl_role, salary, date_of_birth, date_of_start,
            phone_number, city, street, zip_code
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
        """,
        [
            data["empl_surname"],
            data["empl_name"],
            data["empl_patronymic"],
            data["empl_role"],
            data["salary"],
            data["date_of_birth"],
            data["date_of_start"],
            data["phone_number"],
            data["city"],
            data["street"],
            data["zip_code"],
        ],
    )


def get_employee_by_id(employee_id: int):
    return execute_single(
        "SELECT * FROM employees_employee WHERE id = %s", [employee_id]
    )


def update_employee(employee_id: int, data: dict):
    execute_write(
        """
        UPDATE employees_employee SET
            empl_surname = %s, empl_name = %s, empl_patronymic = %s,
            empl_role = %s, salary = %s, date_of_birth = %s,
            date_of_start = %s, phone_number = %s, city = %s,
            street = %s, zip_code = %s
        WHERE id = %s
        """,
        [
            data["empl_surname"],
            data["empl_name"],
            data["empl_patronymic"],
            data["empl_role"],
            data["salary"],
            data["date_of_birth"],
            data["date_of_start"],
            data["phone_number"],
            data["city"],
            data["street"],
            data["zip_code"],
            employee_id,
        ],
    )

def delete_employee(employee_id: int):
    execute_write(
        "DELETE FROM employees_employee WHERE id = %s", [employee_id]
    )
