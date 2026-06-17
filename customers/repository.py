from core.db import execute_query, execute_single, execute_write


def get_distinct_customer_percents() -> list:
    return execute_query(
        "SELECT DISTINCT percent FROM customers_customercard ORDER BY percent"
    )


def get_customer_filters(is_cashier: bool = False):
    if is_cashier:
        return [
            {
                "key": "cust_surname",
                "label": "Search by Surname",
                "type": "search",
                "column": "cust_surname",
            },
        ]
    percents = get_distinct_customer_percents()
    return [
        {
            "key": "percent",
            "label": "Discount %",
            "type": "select",
            "column": "percent",
            "options": [
                {"value": str(p["percent"]), "label": f"{p['percent']}%"}
                for p in percents
            ],
        },
    ]


def get_all_customers(where_sql: str = "", where_params=(), order_by: str = "") -> list:
    return execute_query(
        f"SELECT * FROM customers_customercard{where_sql}{order_by}",
        list(where_params),
    )


def get_customer_by_id(customer_id: int) -> dict | None:
    return execute_single(
        "SELECT * FROM customers_customercard WHERE id = %s",
        [customer_id],
    )


def create_customer(
    cust_surname,
    cust_name,
    cust_patronymic,
    phone_number,
    city,
    street,
    zip_code,
    percent,
) -> None:
    execute_write(
        """
        INSERT INTO customers_customercard
        (cust_surname, cust_name, cust_patronymic, phone_number, city, street, zip_code, percent)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        [
            cust_surname,
            cust_name,
            cust_patronymic,
            phone_number,
            city,
            street,
            zip_code,
            percent,
        ],
    )


def update_customer(customer_card_id: int, data: dict):
    execute_write(
        "UPDATE customers_customercard SET cust_surname = %s, cust_name = %s, cust_patronymic = %s, phone_number = %s, city = %s, street = %s, zip_code = %s, percent = %s WHERE id = %s",
        [
            data["cust_surname"],
            data["cust_name"],
            data["cust_patronymic"],
            data["phone_number"],
            data["city"],
            data["street"],
            data["zip_code"],
            data["percent"],
            customer_card_id,
        ],
    )


def count_checks_for_customer(customer_id: int) -> int:
    result = execute_single(
        "SELECT COUNT(*) as count FROM sales_check WHERE card_id = %s",
        [customer_id],
    )
    return result["count"] if result else 0


def get_check_counts_by_customer() -> dict:
    rows = execute_query(
        "SELECT card_id, COUNT(*) AS count FROM sales_check "
        "WHERE card_id IS NOT NULL GROUP BY card_id"
    )
    return {r["card_id"]: r["count"] for r in rows}


def delete_customer(customer_id: int):
    execute_write("DELETE FROM customers_customercard WHERE id = %s", [customer_id])


def get_top_customers():
    return execute_query(
        """
        SELECT cc.cust_surname, cc.cust_name, cc.phone_number, cc.percent
        FROM customers_customercard cc
        WHERE NOT EXISTS (SELECT *
            FROM products_storeproduct sp
            WHERE sp.promotional_product = False
                AND (SELECT COUNT(*)
                    FROM products_storeproduct sp2
                    WHERE sp2.promotional_product = False
                    AND sp2.selling_price > sp.selling_price) < 5
                AND NOT EXISTS (SELECT *
                                FROM sales_check ch
                                        INNER JOIN sales_sale s ON ch.id = s.check_number_id
                                WHERE ch.card_id = cc.id
                                AND s."UPC" = sp."UPC")
        )
        """
    )
