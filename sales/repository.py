from core.db import execute_query


def get_all_checks(where_sql="", where_params=(), order_by=" ORDER BY print_date DESC"):
    return execute_query(
        f"""
        SELECT c.check_number, c.print_date, c.sum_total, c.vat,
               e.empl_surname, e.empl_name
        FROM sales_check c
        JOIN employees_employee e ON c.id_employee = e.id_employee
        {where_sql}{order_by}
        """,
        list(where_params),
    )


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
