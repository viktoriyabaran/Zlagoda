# Category revenue
CATEGORY_REVENUE_COLUMNS = [
    {"key": "category_name", "label": "Category", "sortable": True},
    {"key": "promotional_product", "label": "Promotional", "sortable": True},
    {"key": "total_units", "label": "Items Sold", "sortable": False},
    {"key": "total_revenue", "label": "Revenue", "sortable": False},
    {
        "key": "percent_of_category_revenue",
        "label": "Share of Category",
        "sortable": False,
    },
]

CATEGORY_REVENUE_SORTABLE = {
    c["key"] for c in CATEGORY_REVENUE_COLUMNS if c["sortable"]
}

# Top customers
TOP_CUSTOMERS_COLUMNS = [
    {"key": "cust_surname", "label": "Surname", "sortable": False},
    {"key": "cust_name", "label": "Name", "sortable": False},
    {"key": "phone_number", "label": "Phone", "sortable": False},
    {"key": "percent", "label": "Discount %", "sortable": False},
]
