from django.urls import NoReverseMatch, reverse

from core.roles import Role

_NAV = [
    (
        "Checks",
        "receipt",
        [
            ("View Checks", "sales:checks", (Role.MANAGER, Role.CASHIER)),
            ("Create Check", "sales:create-check", (Role.CASHIER,)),
        ],
    ),
    (
        "Products",
        "box",
        [
            ("View Products", "products:products", (Role.MANAGER, Role.CASHIER)),
            (
                "View Store Products",
                "products:store-products",
                (Role.MANAGER, Role.CASHIER),
            ),
            ("View Categories", "products:categories", (Role.MANAGER, Role.CASHIER)),
            ("Add Product", "products:add-product", (Role.MANAGER,)),
            ("Add Store Product", "products:add-store-product", (Role.MANAGER,)),
            ("Add Category", "products:add-category", (Role.MANAGER,)),
        ],
    ),
    (
        "Customers",
        "users",
        [
            ("View Customers", "customers:customers", (Role.MANAGER, Role.CASHIER)),
            ("Add Customer", "customers:add-customer", (Role.MANAGER, Role.CASHIER)),
        ],
    ),
    (
        "Employees",
        "badge",
        [
            ("View Employees", "employees:employees", (Role.MANAGER,)),
            ("Add Employee", "employees:add-employee", (Role.MANAGER,)),
        ],
    ),
]


def sidebar_nav(request):
    role = request.session.get("user_role")
    if role not in Role.ALL:
        return {}

    current = request.resolver_match.view_name if request.resolver_match else None

    groups = []
    for label, icon, items in _NAV:
        built = []
        for item_label, url_name, roles in items:
            if role not in roles:
                continue
            try:
                url = reverse(url_name)
            except NoReverseMatch:
                continue
            built.append(
                {"label": item_label, "url": url, "active": url_name == current}
            )
        if built:
            groups.append(
                {
                    "label": label,
                    "icon": icon,
                    "items": built,
                    "active": any(item["active"] for item in built),
                }
            )

    return {"sidebar": {"role": role, "groups": groups}}
