# Categories
CATEGORY_COLUMNS = [
    {"key": "category_name", "label": "Category", "sortable": True},
]

CATEGORY_SORTABLE = {c["key"] for c in CATEGORY_COLUMNS if c["sortable"]}

# Products
PRODUCT_COLUMNS = [
    {"key": "product_name", "label": "Product Name", "sortable": True},
    {"key": "manufacturer", "label": "Manufacturer", "sortable": True},
    {"key": "characteristics", "label": "Characteristics", "sortable": False},
    {"key": "category_name", "label": "Category", "sortable": True},
]

PRODUCT_SORTABLE = {c["key"] for c in PRODUCT_COLUMNS if c["sortable"]}

# Store products
STORE_PRODUCT_COLUMNS = [
    {"key": "UPC", "label": "UPC", "sortable": False},
    {"key": "product_name", "label": "Product Name", "sortable": True},
    {"key": "selling_price", "label": "Price", "sortable": True},
    {"key": "products_number", "label": "Quantity", "sortable": True},
    {"key": "promotional_product", "label": "Promo", "sortable": False},
    {"key": "expiration_date", "label": "Expires", "sortable": True},
]

STORE_PRODUCT_SORTABLE = {c["key"] for c in STORE_PRODUCT_COLUMNS if c["sortable"]}

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
