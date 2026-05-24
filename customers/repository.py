from core.db import execute_query, execute_single, execute_write


def get_all_customers(order_by: str = "") -> list:
    return execute_query(f"SELECT * FROM customers_customercard{order_by}")


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

def delete_customer(customer_id: int):
    execute_write(
        "DELETE FROM customers_customercard WHERE id = %s", [customer_id]
    )
