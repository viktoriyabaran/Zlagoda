from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from .forms import EmployeeForm
from .services import EmployeeService


class AddEmployeeView(View):
    employee_service = EmployeeService()

    def get(self, request):
        return render(
            request,
            "home.html",
            {
                "form": EmployeeForm(),
                "form_title": "Add Employee",
                "form_action": reverse("employees:add-employee"),
            },
        )

    def post(self, request):
        form = EmployeeForm(request.POST)
        if form.is_valid():
            self.employee_service.create_employee(form.cleaned_data)
            return redirect("core:home")
        return render(
            request,
            "home.html",
            {
                "form": form,
                "form_title": "Add Employee",
                "form_action": reverse("employees:add-employee"),
            },
        )
