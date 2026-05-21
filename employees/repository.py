from core.db import execute_write, execute_query


def create_employee(data: dict):
    execute_write(
        """
        INSERT INTO employees_employee (
            id_employee, empl_surname, empl_name, empl_patronymic,
            empl_role, salary, date_of_birth, date_of_start,
            phone_number, city, street, zip_code
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        [
            data["id_employee"],
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


def get_all_employees(order_by: str = ""):
    return execute_query(f"SELECT * FROM employees_employee{order_by}")
