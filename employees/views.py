from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from core.sorting import resolve_sort
from .forms import EmployeeForm
from .services import EmployeeService


EMPLOYEE_COLUMNS = [
    {"key": "empl_surname", "label": "Surname", "sortable": True},
    {"key": "empl_name", "label": "Name", "sortable": False},
    {"key": "empl_role", "label": "Role", "sortable": True},
    {"key": "salary", "label": "Salary", "sortable": True},
    {"key": "phone_number", "label": "Phone", "sortable": False},
]
EMPLOYEE_SORTABLE = {c["key"] for c in EMPLOYEE_COLUMNS if c["sortable"]}


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
            return redirect("employees:employees")
        return render(
            request,
            "home.html",
            {
                "form": form,
                "form_title": "Add Employee",
                "form_action": reverse("employees:add-employee"),
            },
        )


class GetEmployeesView(View):
    employee_service = EmployeeService()

    def get(self, request):
        sort_by, sort_dir = resolve_sort(request, EMPLOYEE_SORTABLE, default="empl_surname")
        rows = self.employee_service.get_all(sort_by, sort_dir)
        return render(
            request,
            "home.html",
            {
                "list": {
                    "title": "EMPLOYEES",
                    "subtitle": "Staff directory",
                    "rows": rows,
                    "columns": EMPLOYEE_COLUMNS,
                    "sort": {"by": sort_by, "dir": sort_dir},
                    "add_url": reverse("employees:add-employee"),
                    "add_label": "Add employee",
                    "empty_message": "No employees yet.",
                },
            },
        )
