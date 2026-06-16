from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from core.decorators import role_required
from core.query_helpers import resolve_sort
from core.roles import Role
from customers.table_config import CUSTOMER_COLUMNS, CUSTOMER_SORTABLE

from .forms import CustomerCardForm
from .services import CustomerService, ICustomerService


@role_required(Role.MANAGER, Role.CASHIER)
class AddCustomerView(View):
    customer_service: ICustomerService = CustomerService()

    def get(self, request):
        return render(
            request,
            "home.html",
            {
                "form": CustomerCardForm(),
                "form_title": "Add Customer",
                "form_action": reverse("customers:add-customer"),
            },
        )

    def post(self, request):
        form = CustomerCardForm(request.POST)
        if form.is_valid():
            self.customer_service.create(form.cleaned_data)
            return redirect("customers:customers")
        return render(
            request,
            "home.html",
            {
                "form": form,
                "form_title": "Add Customer",
                "form_action": reverse("customers:add-customer"),
            },
        )


@role_required(Role.MANAGER, Role.CASHIER)
class GetCustomersView(View):
    customer_service: ICustomerService = CustomerService()

    def get(self, request):
        sort_by, sort_dir = resolve_sort(
            request, CUSTOMER_SORTABLE, default="cust_surname"
        )
        rows = self.customer_service.get_all(sort_by, sort_dir)
        self.customer_service.annotate_deletable(rows)

        return render(
            request,
            "home.html",
            {
                "list": {
                    "title": "CUSTOMERS",
                    "subtitle": "Loyalty card holders",
                    "rows": rows,
                    "columns": CUSTOMER_COLUMNS,
                    "sort": {"by": sort_by, "dir": sort_dir},
                    "add_url": reverse("customers:add-customer"),
                    "add_label": "Add customer",
                    "empty_message": "No customers yet.",
                    "row_id_key": "id",
                    "actions": [
                        {
                            "label": "Edit",
                            "url_name": "customers:edit-customer",
                            "icon": "fa-solid fa-pen",
                        },
                        {
                            "label": "Delete",
                            "url_name": "customers:delete-customer",
                            "icon": "fa-solid fa-trash",
                            "method": "post",
                            "confirm": "Delete this customer?",
                            "roles": [Role.MANAGER],
                            "block_key": "delete_block_reason",
                        },
                    ],
                },
            },
        )


@role_required(Role.MANAGER, Role.CASHIER)
class EditCustomerView(View):
    customer_service: ICustomerService = CustomerService()

    def get(self, request, customer_card_id):
        customer_card = self.customer_service.get_by_id(customer_card_id)
        if not customer_card:
            raise Http404(f"Customer Card with id {customer_card_id} was not found")

        form = CustomerCardForm(
            initial={
                "cust_surname": customer_card["cust_surname"],
                "cust_name": customer_card["cust_name"],
                "cust_patronymic": customer_card["cust_patronymic"],
                "phone_number": customer_card["phone_number"],
                "city": customer_card["city"],
                "street": customer_card["street"],
                "zip_code": customer_card["zip_code"],
                "percent": customer_card["percent"],
            }
        )
        return render(
            request,
            "home.html",
            {
                "form": form,
                "form_title": "Edit Customer Card",
                "form_action": reverse(
                    "customers:edit-customer", args=[customer_card_id]
                ),
                "submit_label": "Save",
            },
        )

    def post(self, request, customer_card_id):
        form = CustomerCardForm(request.POST)
        if form.is_valid():
            self.customer_service.update(customer_card_id, form.cleaned_data)
            return redirect("customers:customers")
        return render(
            request,
            "home.html",
            {
                "form": form,
                "form_title": "Edit Customer Card",
                "form_action": reverse(
                    "customers:edit-customer", args=[customer_card_id]
                ),
                "submit_label": "Save",
            },
        )


@role_required(Role.MANAGER)
class DeleteCustomerView(View):
    customer_service = CustomerService()

    def post(self, request, customer_id):
        try:
            self.customer_service.delete(customer_id)
            return HttpResponse("")
        except ValueError as e:
            return HttpResponse(str(e), status=409)
