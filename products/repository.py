from core.db import (
    execute_insert_returning,
    execute_query,
    execute_single,
    execute_write,
)


def get_product_filters():
    categories = get_all_categories(order_by=" ORDER BY category_name")
    return [
        {
            "key": "category_name",
            "label": "Category",
            "type": "select",
            "column": "c.category_name",
            "options": [
                {"value": c["category_name"], "label": c["category_name"]}
                for c in categories
            ],
        },
        {"key": "date_from", "label": "From", "type": "date"},
        {"key": "date_to", "label": "To", "type": "date"},
    ]


STORE_PRODUCT_FILTERS = [
    {
        "key": "upc",
        "label": "Search by UPC",
        "type": "search",
        "column": 'sp."UPC"',
    },
    {
        "key": "promo",
        "label": "Promo Status",
        "type": "select",
        "column": "sp.promotional_product",
        "options": [
            {"value": "true", "label": "Promotional"},
            {"value": "false", "label": "Non-promotional"},
        ],
    },
]


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


def get_all_products(where_sql="", where_params=(), order_by=""):
    return execute_query(
        f"""
        SELECT p.id, p.product_name, p.manufacturer, p.characteristics, c.category_name
        FROM products_product p
        JOIN products_category c ON p.category_id = c.id
        {where_sql}{order_by}
    """,
        list(where_params),
    )


def create_product(data: dict) -> int:
    product_id = execute_insert_returning(
        "INSERT INTO products_product (category_id, product_name, manufacturer, characteristics) VALUES (%s, %s, %s, %s) RETURNING id",
        [
            data["category"],
            data["product_name"],
            data["manufacturer"],
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
        "UPDATE products_product SET category_id = %s, product_name = %s, manufacturer = %s, characteristics = %s WHERE id = %s",
        [
            data["category"],
            data["product_name"],
            data["manufacturer"],
            data["characteristics"],
            product_id,
        ],
    )


def count_store_products_for_product(product_id: int) -> int:
    result = execute_single(
        "SELECT COUNT(*) as count FROM products_storeproduct WHERE product_id = %s",
        [product_id],
    )
    return result["count"] if result else 0


def get_store_product_counts_by_product() -> dict:
    rows = execute_query(
        "SELECT product_id, COUNT(*) AS count FROM products_storeproduct GROUP BY product_id"
    )
    return {r["product_id"]: r["count"] for r in rows}


def delete_product(product_id: int):
    execute_write("DELETE FROM products_product WHERE id = %s", [product_id])


def get_store_product_by_upc(upc: str):
    return execute_single(
        """
        SELECT sp.*, p.product_name, p.characteristics, p.id as product_code
        FROM products_storeproduct sp
        JOIN products_product p ON sp.product_id = p.id
        WHERE sp."UPC" = %s
        """,
        [upc],
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


def decrement_store_product_number(upc: str, quantity: int):
    execute_write(
        """UPDATE products_storeproduct
           SET products_number = products_number - %s
           WHERE "UPC" = %s""",
        [quantity, upc],
    )


def count_sales_for_store_product(upc: str) -> int:
    result = execute_single(
        'SELECT COUNT(*) as count FROM sales_sale WHERE "UPC" = %s',
        [upc],
    )
    return result["count"] if result else 0


def get_sale_counts_by_store_product() -> dict:
    rows = execute_query(
        'SELECT "UPC", COUNT(*) AS count FROM sales_sale GROUP BY "UPC"'
    )
    return {r["UPC"]: r["count"] for r in rows}


def delete_store_product(upc: str):
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
        [category_id],
    )
    return result["count"] if result else 0


def get_product_counts_by_category() -> dict:
    rows = execute_query(
        "SELECT category_id, COUNT(*) AS count FROM products_product GROUP BY category_id"
    )
    return {r["category_id"]: r["count"] for r in rows}


def get_product_detail(product_id: int) -> dict | None:
    return execute_single(
        """
        SELECT p.id, p.product_name, p.manufacturer, p.characteristics, c.category_name
        FROM products_product p
        JOIN products_category c ON p.category_id = c.id
        WHERE p.id = %s
        """,
        [product_id],
    )


def get_store_product_with_sales(product_id: int) -> dict | None:
    return execute_single(
        """
        SELECT sp."UPC", sp.selling_price, sp.products_number,
               COALESCE(SUM(s.product_number), 0) as total_sold
        FROM products_storeproduct sp
        LEFT JOIN sales_sale s ON s."UPC" = sp."UPC"
        WHERE sp.product_id = %s AND sp.promotional_product = FALSE
        GROUP BY sp."UPC", sp.selling_price, sp.products_number
        """,
        [product_id],
    )


def get_promo_store_product_with_sales(product_id: int) -> dict | None:
    return execute_single(
        """
        SELECT sp."UPC", sp.selling_price, sp.products_number,
               COALESCE(SUM(s.product_number), 0) as total_sold
        FROM products_storeproduct sp
        LEFT JOIN sales_sale s ON s."UPC" = sp."UPC"
        WHERE sp.product_id = %s AND sp.promotional_product = TRUE
        GROUP BY sp."UPC", sp.selling_price, sp.products_number
        """,
        [product_id],
    )
