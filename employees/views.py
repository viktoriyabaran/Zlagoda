from django.shortcuts import redirect, render
from django.views import View

from .forms import EmployeeForm
from .services import EmployeeService


class AddEmployeeView(View):
    employee_service = EmployeeService()

    def get(self, request):
        form = EmployeeForm()
        return render(request, "employees/add-employee.html", {"form": form})

    def post(self, request):
        form = EmployeeForm(request.POST)
        if form.is_valid():
            self.employee_service.create_employee(form.cleaned_data)
            return redirect("employees:employees")
        return render(request, "employees/add-employee.html", {"form": form})
