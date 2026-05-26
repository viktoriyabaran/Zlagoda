# Define sales views here

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from core.decorators import login_required
from employees.repository import get_all_cashiers
from products.repository import get_all_store_products, get_store_product_by_upc

from .services import CheckService


@login_required
class GetChecksView(View):
    check_service = CheckService()

    def get(self, request):
        date_from = request.GET.get("date_from")
        date_to = request.GET.get("date_to")
        employee_id = request.GET.get("employee_id")

        cashiers = get_all_cashiers()

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
                        {"key": "id", "label": "Check #", "sortable": False},
                        {"key": "print_date", "label": "Date", "sortable": False},
                        {"key": "empl_surname", "label": "Cashier", "sortable": False},
                        {"key": "sum_total", "label": "Total", "sortable": False},
                        {"key": "vat", "label": "VAT", "sortable": False},
                    ],
                    "sort": {"by": "print_date", "dir": "desc"},
                    "empty_message": "No checks found.",
                    "row_id_key": "id",
                    "filters": [
                        {"key": "date_from", "label": "From date", "type": "date"},
                        {"key": "date_to", "label": "To date", "type": "date"},
                        {
                            "key": "employee_id",
                            "label": "Cashier",
                            "type": "select",
                            "column": "employee_id",
                            "options": [
                                {
                                    "value": str(c["id"]),
                                    "label": f"{c['empl_surname']} {c['empl_name']}",
                                }
                                for c in cashiers
                            ],
                        },
                    ],
                    "actions": [
                        {
                            "label": "View",
                            "url_name": "sales:check-detail",
                            "icon": "👁",
                        },
                        {
                            "label": "Delete",
                            "url_name": "sales:delete-check",
                            "icon": "✕",
                            "method": "post",
                            "confirm": "Are you sure you want to permanently delete this check? This action will also delete all related sale records.",
                        },
                    ],
                },
                "check_items": check_items,
                "date_from": date_from or "",
                "date_to": date_to or "",
                "employee_id": employee_id or "",
            },
        )


class DeleteCheckView(View):
    check_service = CheckService()

    def post(self, request, check_id):
        self.check_service.delete_check(check_id)
        return HttpResponse("")


class CreateCheckView(View):
    check_service = CheckService()

    def get(self, request):
        request.session.pop("current_check_id", None)
        request.session.pop("current_check_items", None)
        return redirect("sales:add-item")


class AddItemToCheckView(View):
    check_service = CheckService()

    def get(self, request):
        items = request.session.get("current_check_items", [])
        for item in items:
            item["total"] = float(item["selling_price"]) * item["product_number"]
        store_products = get_all_store_products()
        sum_total = sum(float(i["selling_price"]) * i["product_number"] for i in items)
        vat = round(sum_total * 0.2, 4)
        return render(
            request,
            "sales/create_check.html",
            {
                "items": items,
                "store_products": store_products,
                "sum_total": sum_total,
                "vat": vat,
            },
        )

    def post(self, request):
        upc = request.POST.get("upc")
        product_number = int(request.POST.get("product_number", 1))

        product = get_store_product_by_upc(upc)
        if not product:
            return redirect("sales:add-item")

        items = request.session.get("current_check_items", [])
        items.append(
            {
                "upc": upc,
                "product_name": product["product_name"],
                "selling_price": str(product["selling_price"]),
                "product_number": product_number,
                "promotional_product": product["promotional_product"],
            }
        )
        request.session["current_check_items"] = items
        return redirect("sales:add-item")


class FinalizeCheckView(View):
    check_service = CheckService()

    def post(self, request):
        items = request.session.get("current_check_items", [])
        if not items:
            return redirect("sales:add-item")

        user_id = request.session.get("user_id")
        check_id = self.check_service.start_check(user_id)

        for item in items:
            self.check_service.add_item(
                check_id, item["upc"], item["product_number"], item["selling_price"]
            )

        self.check_service.finalize_check(check_id, items)

        request.session.pop("current_check_id", None)
        request.session.pop("current_check_items", None)

        return redirect("sales:checks")


class GetCheckDetailView(View):
    check_service = CheckService()

    def get(self, request, check_id):
        items = self.check_service.get_items(check_id)
        return render(
            request,
            "sales/check_detail.html",
            {
                "check_id": check_id,
                "items": items,
            },
        )
