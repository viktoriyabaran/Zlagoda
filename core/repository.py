from core.db import execute_single, execute_write


def get_user_by_username(username: str):
    return execute_single(
        "SELECT u.*, e.empl_role "
        "FROM core_user u LEFT JOIN employees_employee e ON e.id = u.employee_id "
        "WHERE u.username = %s",
        [username],
    )


def get_user_by_id(user_id: int):
    return execute_single("SELECT * FROM core_user WHERE id = %s", [user_id])


def create_user(username: str, password_hash: str, employee_id: int):
    execute_write(
        "INSERT INTO core_user (username, password, employee_id) VALUES (%s, %s, %s)",
        [username, password_hash, employee_id],
    )
