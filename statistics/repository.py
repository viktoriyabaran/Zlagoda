from core.db import execute_query


def get_customer_purchase_stats() -> list:
    return execute_query(
        """
        SELECT cc.id, cc.cust_surname, cc.cust_name,
               COUNT(ch.id) AS check_count,
               SUM(ch.sum_total) AS total_sum
        FROM customers_customercard cc
        INNER JOIN sales_check ch ON cc.id = ch.card_id
        INNER JOIN sales_sale s ON ch.id = s.check_number_id
        GROUP BY cc.id, cc.cust_surname, cc.cust_name
        """
    )


def get_cashiers_served_all_customers(employee_id: int = None) -> list:
    sql = """
        SELECT e.id, e.empl_surname, e.empl_name
        FROM employees_employee AS e
        WHERE NOT EXISTS (
            SELECT cc.id
            FROM customers_customercard cc
            WHERE NOT EXISTS (
                SELECT ch.id
                FROM sales_check ch
                WHERE ch.employee_id = e.id
                  AND ch.card_id = cc.id
            )
        )
    """
    if employee_id:
        sql += " AND e.id = %s"
        return execute_query(sql, [employee_id])
    return execute_query(sql)
