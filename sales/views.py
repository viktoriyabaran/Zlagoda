# Define sales views here

from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.views import View

from core.decorators import role_required
from core.repository import get_user_by_id
from core.roles import Role
from customers.repository import get_all_customers
from employees.repository import get_all_cashiers, get_employee_by_id
from products.repository import (
    decrement_store_product_number,
    get_all_store_products,
    get_store_product_by_upc,
)

from .repository import update_check_totals
from .services import CheckService
from .table_config import CHECK_COLUMNS


@role_required(Role.MANAGER, Role.CASHIER)
class GetChecksView(View):
    check_service = CheckService()

    def get(self, request):
        date_from = request.GET.get("date_from")
        date_to = request.GET.get("date_to")

        is_cashier = request.session.get("user_role") == Role.CASHIER
        if is_cashier:
            # Cashiers only ever see their own checks, regardless of any filter.
            employee = get_user_by_id(request.session["user_id"])
            if not employee:
                return redirect("core:login")
            employee_id = employee["employee_id"]
        else:
            employee_id = request.GET.get("employee_id")

        checks = self.check_service.get_all(
            date_from=date_from,
            date_to=date_to,
            employee_id=employee_id or None,
        )

        total_sum = sum(float(c["sum_total"]) for c in checks) if checks else 0

        selected_check_id = request.GET.get("check_id")
        check_items = []
        if selected_check_id:
            if is_cashier:
                check = self.check_service.get_by_id(int(selected_check_id))
                owns_check = check and check["employee_id"] == employee_id
            else:
                owns_check = True
            if owns_check:
                check_items = self.check_service.get_items(int(selected_check_id))

        filters: list[dict] = [
            {"key": "date_from", "label": "From date", "type": "date"},
            {"key": "date_to", "label": "To date", "type": "date"},
        ]
        actions: list[dict] = [
            {
                "label": "View",
                "url_name": "sales:check-detail",
                "icon": "fa-solid fa-eye",
            },
        ]
        if not is_cashier:
            cashiers = get_all_cashiers()
            filters.insert(
                0,
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
            )
            actions.append(
                {
                    "label": "Delete",
                    "url_name": "sales:delete-check",
                    "icon": "fa-solid fa-trash",
                    "method": "post",
                    "confirm": "Are you sure you want to permanently delete this check? This action will also delete all related sale records.",
                }
            )

        return render(
            request,
            "home.html",
            {
                "list": {
                    "title": "CHECKS",
                    "subtitle": "My sales" if is_cashier else "Sales history",
                    "rows": checks,
                    "columns": CHECK_COLUMNS,
                    "sort": {"by": "print_date", "dir": "desc"},
                    "empty_message": "No checks found.",
                    "has_date_filter": True,
                    "row_id_key": "id",
                    "filters": filters,
                    "actions": actions,
                    "total_sum": total_sum,
                },
                "check_items": check_items,
                "date_from": date_from or "",
                "date_to": date_to or "",
                "employee_id": employee_id or "",
                "total_sum": total_sum,
            },
        )


@role_required(Role.MANAGER)
class DeleteCheckView(View):
    check_service = CheckService()

    def post(self, request, check_id):
        self.check_service.delete_check(check_id)
        return HttpResponse("")


@role_required(Role.CASHIER)
class CreateCheckView(View):
    check_service = CheckService()

    def get(self, request):
        request.session.pop("current_check_id", None)
        request.session.pop("current_check_items", None)
        return redirect("sales:add-item")


def render_check_page(request):
    check_service = CheckService()
    items = request.session.get("current_check_items", [])
    in_check = {}
    for item in items:
        item["total"] = float(item["selling_price"]) * item["quantity"]
        in_check[item["upc"]] = in_check.get(item["upc"], 0) + item["quantity"]

    store_products = get_all_store_products()
    for p in store_products:
        p["available"] = p["products_number"] - in_check.get(p["UPC"], 0)

    session_card = request.session.get("current_check_card")
    selected_card = str(session_card).strip() if session_card else None

    discount_percent = check_service.resolve_discount_percent(selected_card)
    totals = check_service.compute_totals(items, discount_percent)

    return render(
        request,
        "sales/create_check.html",
        {
            "items": items,
            "store_products": store_products,
            "customer_cards": get_all_customers(),
            "selected_card": selected_card,
            **totals,
        },
    )


@role_required(Role.CASHIER)
class AddItemToCheckView(View):
    check_service = CheckService()

    def get(self, request):
        return render_check_page(request)

    def post(self, request):
        upc = request.POST.get("upc")
        quantity = int(request.POST.get("quantity", 1))

        card_id = request.POST.get("card_id")
        if card_id is not None:
            request.session["current_check_card"] = card_id if card_id else None

        product = get_store_product_by_upc(upc)
        if not product or quantity < 1:
            return redirect("sales:add-item")

        items = request.session.get("current_check_items", [])
        existing = next((i for i in items if i["upc"] == upc), None)
        already_in_check = existing["quantity"] if existing else 0

        available = product["products_number"] - already_in_check
        if quantity > available:
            return HttpResponse(
                f"Not enough stock: only {available} more unit(s) of "
                f"{product['product_name']} available.",
                status=409,
            )

        if existing:
            existing["quantity"] += quantity
        else:
            items.append(
                {
                    "upc": upc,
                    "product_name": product["product_name"],
                    "selling_price": str(product["selling_price"]),
                    "quantity": quantity,
                    "promotional_product": product["promotional_product"],
                }
            )
        request.session["current_check_items"] = items
        return render_check_page(request)


@role_required(Role.CASHIER)
class UpdateCheckItemView(View):
    def post(self, request):
        upc = request.POST.get("upc")
        quantity = int(request.POST.get("quantity", 1))
        items = request.session.get("current_check_items", [])
        item = next((i for i in items if i["upc"] == upc), None)
        if not item:
            return render_check_page(request)

        if quantity < 1:
            items = [i for i in items if i["upc"] != upc]
            request.session["current_check_items"] = items
            return render_check_page(request)

        product = get_store_product_by_upc(upc)
        if product and quantity > product["products_number"]:
            return HttpResponse(
                f"Not enough stock: only {product['products_number']} unit(s) of "
                f"{product['product_name']} available.",
                status=409,
            )

        item["quantity"] = quantity
        request.session["current_check_items"] = items
        return render_check_page(request)


@role_required(Role.CASHIER)
class RemoveCheckItemView(View):
    def post(self, request):
        upc = request.POST.get("upc")
        items = request.session.get("current_check_items", [])
        request.session["current_check_items"] = [i for i in items if i["upc"] != upc]
        return render_check_page(request)


@role_required(Role.CASHIER)
class ApplyCardView(View):
    check_service = CheckService()

    def post(self, request):
        card_id = request.POST.get("card_id")
        request.session["current_check_card"] = card_id if card_id else None

        items = request.session.get("current_check_items", [])
        discount_percent = self.check_service.resolve_discount_percent(card_id)
        totals = self.check_service.compute_totals(items, discount_percent)
        return render(request, "sales/_check_summary.html", totals)


@role_required(Role.CASHIER)
class FinalizeCheckView(View):
    check_service = CheckService()

    def post(self, request):
        items = request.session.get("current_check_items", [])
        if not items:
            return redirect("sales:add-item")

        user_id = request.session.get("user_id")
        card_id = request.session.get("current_check_card")
        check_id = self.check_service.start_check(user_id, card_id=card_id)

        for item in items:
            self.check_service.add_item(
                check_id, item["upc"], item["quantity"], item["selling_price"]
            )
            decrement_store_product_number(item["upc"], item["quantity"])

        discount_percent = self.check_service.resolve_discount_percent(card_id)
        totals = self.check_service.compute_totals(items, discount_percent)
        update_check_totals(check_id, totals["sum_total"], totals["vat"])

        request.session.pop("current_check_id", None)
        request.session.pop("current_check_items", None)
        request.session.pop("current_check_card", None)

        if request.POST.get("action") == "new":
            return redirect("sales:add-item")
        return redirect("sales:checks")


@role_required(Role.MANAGER, Role.CASHIER)
class GetCheckDetailView(View):
    check_service = CheckService()

    def get(self, request, check_id):
        check = self.check_service.get_by_id(check_id)
        if not check:
            return HttpResponseForbidden("Check not found.")

        if request.session.get("user_role") == Role.CASHIER:
            employee = get_user_by_id(request.session["user_id"])
            if not employee:
                return redirect("core:login")
            employee_id = employee["employee_id"]
            if check["employee_id"] != employee_id:
                return HttpResponseForbidden(
                    "Viewing this resource is not allowed for you."
                )
        items = self.check_service.get_items(check_id)

        for item in items:
            item["subtotal"] = "{:.4f}".format(
                float(item["selling_price"]) * item["product_number"]
            )

        cashier = get_employee_by_id(check["employee_id"])
        cashier_name = (
            f"{cashier['empl_surname']} {cashier['empl_name']}" if cashier else "—"
        )

        customer_name = "No Card"
        if check["card_id"]:
            card = next(
                (c for c in get_all_customers() if c["id"] == check["card_id"]), None
            )
            if card:
                customer_name = f"{card['cust_surname']} {card['cust_name']}"

        discount_percent = self.check_service.resolve_discount_percent(check["card_id"])
        items_for_totals = [
            {"selling_price": item["selling_price"], "quantity": item["product_number"]}
            for item in items
        ]
        totals = self.check_service.compute_totals(items_for_totals, discount_percent)

        return render(
            request,
            "sales/check_detail.html",
            {
                "check_id": check_id,
                "items": items,
                "cashier_name": cashier_name,
                "customer_name": customer_name,
                "print_date": check["print_date"],
                **totals,
            },
        )
