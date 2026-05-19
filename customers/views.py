from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from .forms import CustomerCardForm
from .services import CustomerService

class AddCustomerView(View):
    customer_service = CustomerService()

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

class GetCustomersView(View):
    customer_service = CustomerService()

    def get(self, request):
        all_customers = self.customer_service.get_all()
        return render(request, "customers/customers.html", {"customers": all_customers})
