CUSTOMER_COLUMNS = [
    {"key": "id", "label": "Card Number", "sortable": False},
    {"key": "cust_surname", "label": "Surname", "sortable": True},
    {"key": "cust_name", "label": "Name", "sortable": False},
    {"key": "phone_number", "label": "Phone", "sortable": False},
    {"key": "percent", "label": "Discount %", "sortable": False},
]
CUSTOMER_SORTABLE = {c["key"] for c in CUSTOMER_COLUMNS if c["sortable"]}
