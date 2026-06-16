from django.shortcuts import render

from core.decorators import role_required
from core.roles import Role

from .services import StatisticsService

_service = StatisticsService()


@role_required(Role.MANAGER)
def customer_purchase_stats(request):
    rows = _service.get_customer_purchase_stats()
    return render(
        request,
        "home.html",
        {
            "list": {
                "title": "CUSTOMER PURCHASE STATISTICS",
                "subtitle": "Number of checks and total amount per loyalty card holder",
                "columns": [
                    {"key": "id", "label": "Card Number"},
                    {"key": "cust_surname", "label": "Surname"},
                    {"key": "cust_name", "label": "Name"},
                    {"key": "check_count", "label": "Number of Checks"},
                    {"key": "total_sum", "label": "Total Amount"},
                ],
                "rows": rows,
                "empty_message": "No data available.",
            }
        },
    )


@role_required(Role.MANAGER)
def cashiers_served_all_customers(request):
    surname = request.GET.get("surname") or None

    rows = _service.get_cashiers_served_all_customers(surname)
    return render(
        request,
        "home.html",
        {
            "list": {
                "title": "CASHIERS WHO SERVED ALL CUSTOMERS",
                "subtitle": "Cashiers that have served every loyalty card holder",
                "columns": [
                    {"key": "id", "label": "Employee ID", "sortable": False},
                    {"key": "empl_surname", "label": "Surname", "sortable": False},
                    {"key": "empl_name", "label": "Name", "sortable": False},
                ],
                "rows": rows,
                "empty_message": "No cashiers have served all customers yet.",
                "row_id_key": "id",
                "filters": [
                    {"key": "surname", "type": "search", "label": "Search by surname"},
                ],
            }
        },
    )
