from core.db import execute_single


def get_user_by_username(username: str):
    return execute_single("SELECT * FROM core_user WHERE username = %s", [username])


def get_user_by_id(user_id: int):
    return execute_single("SELECT * FROM core_user WHERE id = %s", [user_id])
