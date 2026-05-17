from django.shortcuts import redirect, render
from django.views import View

from core.decorators import login_required
from .forms import CustomerCardForm
from .services import CustomerService

class AddCustomerView(View):
    customer_service = CustomerService()

    def get(self, request):
        form = CustomerCardForm()
        return render(request, "customers/add-customer.html", {"form": form})

    def post(self, request):
        form = CustomerCardForm(request.POST)
        if form.is_valid():
            self.customer_service.create(form.cleaned_data)
            return redirect("customers:customers")
        return render(request, "customers/add-customer.html", {"form": form})


@login_required
def customers(request):
    service = CustomerService()
    all_customers = service.get_all()
    return render(request, "customers/customers.html", {"customers": all_customers})
