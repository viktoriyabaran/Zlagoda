from core.db import execute_insert_returning, execute_query, execute_single, execute_write


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


def get_all_products(order_by: str = ""):
    return execute_query(f"""
        SELECT p.id_product, p.product_name, p.characteristics, c.category_name
        FROM products_product p
        JOIN products_category c ON p.category_number_id = c.category_number
        {order_by}
    """)

def create_product(data: dict) -> int:
    return execute_insert_returning(
        "INSERT INTO products_product (category_id, product_name, characteristics) VALUES (%s, %s, %s) RETURNING id",
        [
            data["category"],
            data["product_name"],
            data["characteristics"],
        ],
    )


def get_store_product_by_upc(upc: str):
    return execute_single(
        'SELECT * FROM products_storeproduct WHERE "UPC" = %s', [upc]
    )


def get_store_products_by_product(product_id):
    return execute_query(
        "SELECT * FROM products_storeproduct WHERE product_id = %s", [product_id]
    )


def create_store_product(data: dict):
    execute_write(
        '''INSERT INTO products_storeproduct
           ("UPC", "UPC_prom_id", product_id, selling_price, products_number, promotional_product)
           VALUES (%s, %s, %s, %s, %s, %s)''',
        [
            data["UPC"],
            data["UPC_prom"],
            data["product"],
            data["selling_price"],
            data["products_number"],
            data["promotional_product"],
        ],
    )
