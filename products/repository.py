from core.db import execute_single, execute_query, execute_write

def get_category_by_id(category_id: int):
    return execute_single("SELECT * FROM products_category WHERE id = %s", [category_id])

def get_all_categories():
    return execute_query("SELECT * FROM products_category")

def create_category(category_name: str):
    execute_write(
        "INSERT INTO products_category (category_name) VALUES (%s)",
        [category_name],
    )
