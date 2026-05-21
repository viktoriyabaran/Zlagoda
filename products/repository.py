from core.db import execute_query, execute_single, execute_write


def get_category_by_id(category_id: int):
    return execute_single(
        "SELECT * FROM products_category WHERE id = %s", [category_id]
    )


def get_all_categories(order_by: str = ""):
    return execute_query(f"SELECT * FROM products_category{order_by}")


def create_category(category_name: str):
    execute_write(
        "INSERT INTO products_category (category_name) VALUES (%s)",
        [category_name],
    )


def get_all_products():
    return execute_query(
        "SELECT id_product, product_name FROM products_product ORDER BY product_name"
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


def get_store_product_by_upc(upc: str):
    return execute_single(
        'SELECT * FROM products_storeproduct WHERE "UPC" = %s', [upc]
    )


def get_store_products_by_product(id_product):
    return execute_query(
        "SELECT * FROM products_storeproduct WHERE id_product_id = %s", [id_product]
    )


def create_store_product(data: dict):
    execute_write(
        '''INSERT INTO products_storeproduct
           ("UPC", "UPC_prom_id", id_product_id, selling_price, products_number, promotional_product)
           VALUES (%s, %s, %s, %s, %s, %s)''',
        [
            data["UPC"],
            data["UPC_prom"],
            data["id_product"],
            data["selling_price"],
            data["products_number"],
            data["promotional_product"],
        ],
    )
