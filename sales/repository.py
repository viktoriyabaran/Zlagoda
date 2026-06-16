from core.db import (
    execute_insert_returning,
    execute_query,
    execute_single,
    execute_write,
)


def get_all_checks(where_sql="", where_params=(), order_by=" ORDER BY print_date DESC"):
    return execute_query(
        f"""
        SELECT c.id, c.print_date, c.sum_total, c.vat,
               e.empl_surname, e.empl_name
        FROM sales_check c
        JOIN employees_employee e ON c.employee_id = e.id
        {where_sql}{order_by}
        """,
        list(where_params),
    )


def get_check_by_id(check_id: int):
    return execute_single("SELECT * FROM sales_check WHERE id = %s", [check_id])


def get_check_items(check_id: int):
    return execute_query(
        """
        SELECT p.product_name, s.product_number, s.selling_price
        FROM sales_sale s
        JOIN products_storeproduct sp ON s."UPC" = sp."UPC"
        JOIN products_product p ON sp.product_id = p.id
        WHERE s.check_number_id = %s
        """,
        [check_id],
    )


def delete_check_by_id(check_id: str):
    execute_write("DELETE FROM sales_check WHERE id = %s", [check_id])


def create_check(employee_id: int, card_id=None) -> int | None:
    return execute_insert_returning(
        """
        INSERT INTO sales_check (employee_id, card_id, print_date, sum_total, vat)
        VALUES (%s, %s, NOW(), 0, 0)
        RETURNING id
        """,
        [employee_id, card_id],
    )


def add_sale_to_check(check_id: int, upc: str, product_number: int, selling_price):
    execute_write(
        """
        INSERT INTO sales_sale ("UPC", check_number_id, product_number, selling_price)
        VALUES (%s, %s, %s, %s)
        """,
        [upc, check_id, product_number, selling_price],
    )


def update_check_totals(check_id: int, sum_total, vat):
    execute_write(
        "UPDATE sales_check SET sum_total = %s, vat = %s WHERE id = %s",
        [sum_total, vat, check_id],
    )


def get_total_units_sold(product_id: int, date_from: str, date_to: str):
    return execute_single(
        """
        SELECT SUM(s.product_number) as total_units
        FROM sales_sale s
        JOIN products_storeproduct sp ON s."UPC" = sp."UPC"
        WHERE sp.product_id = %s
          AND s.check_number_id IN (
              SELECT id FROM sales_check
              WHERE print_date >= %s AND print_date <= %s
          )
        """,
        [product_id, date_from, date_to],
    )


def get_category_revenue_stats(order_by: str = "", promotional=None):
    outer_where = ""
    params: list = []
    if promotional is not None:
        outer_where = " WHERE sp.promotional_product = %s"
        params.append(promotional)

    return execute_query(
        f"""
        SELECT c.category_name, sp.promotional_product, SUM(s.product_number) AS total_units,
            SUM(s.selling_price * s.product_number) AS total_revenue,
            ROUND(
                SUM(s.selling_price * s.product_number) / (
                    SELECT SUM(s1.selling_price * s1.product_number)
                    FROM products_product p1
                    INNER JOIN products_storeproduct sp1
                        ON sp1.product_id = p1.id
                    INNER JOIN sales_sale s1
                        ON s1."UPC" = sp1."UPC"
                    WHERE p1.category_id = c.id
                ) * 100,
                2
            )::text || '%%' AS percent_of_category_revenue
        FROM products_category c
        INNER JOIN products_product p ON p.category_id = c.id
        INNER JOIN products_storeproduct sp ON sp.product_id = p.id
        INNER JOIN sales_sale s ON s."UPC" = sp."UPC"
        {outer_where}
        GROUP BY c.category_name, c.id, sp.promotional_product
        {order_by}
        """,
        params,
    )
