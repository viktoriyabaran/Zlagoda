# Define sales views here

from django.shortcuts import render
from django.views import View

from .services import CheckService


class GetChecksView(View):
    check_service = CheckService()

    def get(self, request):
        date_from = request.GET.get("date_from")
        date_to = request.GET.get("date_to")
        employee_id = request.GET.get("employee_id")

        checks = self.check_service.get_all(
            date_from=date_from,
            date_to=date_to,
            employee_id=employee_id or None,
        )

        selected_check_id = request.GET.get("check_id")
        check_items = []
        if selected_check_id:
            check_items = self.check_service.get_items(int(selected_check_id))

        return render(
            request,
            "home.html",
            {
                "list": {
                    "title": "CHECKS",
                    "subtitle": "Sales history",
                    "rows": checks,
                    "columns": [
                        {"key": "check_number", "label": "Check #", "sortable": False},
                        {"key": "print_date", "label": "Date", "sortable": False},
                        {"key": "empl_surname", "label": "Cashier", "sortable": False},
                        {"key": "sum_total", "label": "Total", "sortable": False},
                        {"key": "vat", "label": "VAT", "sortable": False},
                    ],
                    "sort": {"by": "print_date", "dir": "desc"},
                    "empty_message": "No checks found.",
                    "row_id_key": "id",
                },
                "check_items": check_items,
                "date_from": date_from or "",
                "date_to": date_to or "",
                "employee_id": employee_id or "",
            },
        )
