from core.db import execute_single, execute_write


def get_user_by_username(username: str):
    return execute_single("SELECT * FROM core_user WHERE username = %s", [username])


def get_user_by_id(user_id: int):
    return execute_single("SELECT * FROM core_user WHERE id = %s", [user_id])


def create_user(username: str, password_hash: str, id_employee: str):
    execute_write(
        "INSERT INTO core_user (username, password, id_employee) VALUES (%s, %s, %s)",
        [username, password_hash, id_employee],
    )
