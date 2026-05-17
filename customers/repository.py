from core.db import execute_query, execute_single, execute_write

def get_all_customers():
    return execute_query("SELECT * FROM customers_customercard")


def get_customer_by_card(card_number: str):
    return execute_single(
        "SELECT * FROM customers_customercard WHERE card_number = %s",
        [card_number],
    )

def create_customer(card_number, cust_surname, cust_name, cust_patronymic, phone_number, city, street, zip_code, percent):
    execute_write(
        """
        INSERT INTO customers_customercard
        (card_number, cust_surname, cust_name, cust_patronymic, phone_number, city, street, zip_code, percent)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        [card_number, cust_surname, cust_name, cust_patronymic, phone_number, city, street, zip_code, percent],
    )
