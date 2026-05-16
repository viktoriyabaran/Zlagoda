from core.db import execute_single, execute_all, execute_update

def get_category_by_id(user_id: int):
    return execute_single("SELECT * FROM products_category WHERE id = %s", [category_id])

def get_all_categories():
    return execute_all("SELECT * FROM products_category")

def create_category(category_name: str):
    execute_update(
        "INSERT INTO products_category (category_name) VALUES (%s)",
        [category_name],
    )
