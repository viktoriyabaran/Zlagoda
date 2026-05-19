from core.db import execute_query, execute_single, execute_write


def get_category_by_id(category_id: int):
    return execute_single(
        "SELECT * FROM products_category WHERE id = %s", [category_id]
    )


def get_all_categories():
    return execute_query("SELECT * FROM products_category")


def create_category(category_name: str):
    execute_write(
        "INSERT INTO products_category (category_name) VALUES (%s)",
        [category_name],
    )


def create_product(data: dict):
    execute_write(
        "INSERT INTO products_product (id_product, category_number_id, product_name, characteristics) VALUES (%s, %s, %s, %s)",
        [
            data["id_product"],
            data["category_number"],
            data["product_name"],
            data["characteristics"],
        ],
    )
