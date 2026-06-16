EMPLOYEE_COLUMNS = [
    {"key": "empl_surname", "label": "Surname", "sortable": True},
    {"key": "empl_name", "label": "Name", "sortable": False},
    {"key": "empl_role", "label": "Role", "sortable": True},
    {"key": "salary", "label": "Salary", "sortable": True},
    {"key": "phone_number", "label": "Phone", "sortable": False},
]

EMPLOYEE_SORTABLE = {c["key"] for c in EMPLOYEE_COLUMNS if c["sortable"]}

EMPLOYEE_FILTERS = [
    {"key": "q", "label": "Search surname", "type": "search", "column": "empl_surname"},
    {
        "key": "role",
        "label": "Role",
        "type": "select",
        "column": "empl_role",
        "options": [
            {"value": "Cashier", "label": "Cashier"},
            {"value": "Manager", "label": "Manager"},
        ],
    },
]
