from core.db import (
    execute_insert_returning,
    execute_query,
    execute_single,
    execute_write,
)


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


def delete_category(category_id: int):
    execute_write("DELETE FROM products_category WHERE id = %s", [category_id])


def get_all_products(order_by: str = ""):
    return execute_query(f"""
        SELECT p.id, p.product_name, p.characteristics, c.category_name
        FROM products_product p
        JOIN products_category c ON p.category_id = c.id
        {order_by}
    """)


def create_product(data: dict) -> int:
    product_id = execute_insert_returning(
        "INSERT INTO products_product (category_id, product_name, characteristics) VALUES (%s, %s, %s) RETURNING id",
        [
            data["category"],
            data["product_name"],
            data["characteristics"],
        ],
    )

    if not isinstance(product_id, int):
        raise TypeError(
            "Repository returned did not return an integer pk: ", type(product_id)
        )

    return product_id


def get_product_by_id(product_id: int) -> dict | None:
    return execute_single("SELECT * FROM products_product WHERE id = %s", [product_id])


def update_product(product_id: int, data: dict):
    execute_write(
        "UPDATE products_product SET category_id = %s, product_name = %s, characteristics = %s WHERE id = %s",
        [data["category"], data["product_name"], data["characteristics"], product_id],
    )


def delete_product(product_id: int):
    execute_write(
        """DELETE FROM sales_sale WHERE "UPC" IN (
            SELECT "UPC" FROM products_storeproduct WHERE product_id = %s
        )""",
        [product_id],
    )
    execute_write(
        "DELETE FROM products_storeproduct WHERE product_id = %s", [product_id]
    )
    execute_write("DELETE FROM products_product WHERE id = %s", [product_id])


def get_store_product_by_upc(upc: str):
    return execute_single(
        """
        SELECT sp.*, p.product_name
        FROM products_storeproduct sp
        JOIN products_product p ON sp.product_id = p.id
        WHERE sp."UPC" = %s
        """,
        [upc]
    )


def get_store_products_by_product(product_id):
    return execute_query(
        "SELECT * FROM products_storeproduct WHERE product_id = %s", [product_id]
    )


def create_store_product(data: dict):
    execute_write(
        """INSERT INTO products_storeproduct
           ("UPC", "UPC_prom_id", product_id, selling_price, products_number, promotional_product)
           VALUES (%s, %s, %s, %s, %s, %s)""",
        [
            data["UPC"],
            data["UPC_prom"],
            data["product"],
            data["selling_price"],
            data["products_number"],
            data["promotional_product"],
        ],
    )


def get_all_store_products(where_sql="", where_params=(), order_by=""):
    return execute_query(
        f"""
        SELECT sp."UPC", p.product_name, p.characteristics,
               sp.selling_price, sp.products_number, sp.promotional_product
        FROM products_storeproduct sp
        JOIN products_product p ON sp.product_id = p.id
        {where_sql}{order_by}
    """,
        list(where_params),
    )


def update_store_product(upc: str, data: dict):
    execute_write(
        """UPDATE products_storeproduct
           SET selling_price = %s, products_number = %s, promotional_product = %s
           WHERE "UPC" = %s""",
        [
            data["selling_price"],
            data["products_number"],
            data["promotional_product"],
            upc,
        ],
    )


def delete_store_product(upc: str):
    execute_write('DELETE FROM sales_sale WHERE "UPC" = %s', [upc])
    execute_write('DELETE FROM products_storeproduct WHERE "UPC" = %s', [upc])


def update_category(category_id: int, category_name: str):
    execute_write(
        "UPDATE products_category SET category_name = %s WHERE id = %s",
        [category_name, category_id],
    )

def get_promotional_store_products(order_by=""):
    return execute_query(
        f"""
        SELECT sp."UPC", p.product_name, p.characteristics,
               sp.selling_price, sp.products_number, sp.promotional_product
        FROM products_storeproduct sp
        JOIN products_product p ON sp.product_id = p.id
        WHERE sp.promotional_product = TRUE
        {order_by}
        """,
    )

def get_non_promotional_store_products(order_by=""):
    return execute_query(
        f"""
        SELECT sp."UPC", p.product_name, p.characteristics,
               sp.selling_price, sp.products_number, sp.promotional_product
        FROM products_storeproduct sp
        JOIN products_product p ON sp.product_id = p.id
        WHERE sp.promotional_product = FALSE
        {order_by}
        """,
    )

def count_products_in_category(category_id: int) -> int:
    result = execute_single(
        "SELECT COUNT(*) as count FROM products_product WHERE category_id = %s",
        [category_id]
    )
    return result["count"] if result else 0
