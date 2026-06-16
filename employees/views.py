from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from core.decorators import role_required
from core.query_helpers import resolve_sort
from core.roles import Role

from .forms import EmployeeForm
from .services import EmployeeService
from .table_config import EMPLOYEE_COLUMNS, EMPLOYEE_FILTERS, EMPLOYEE_SORTABLE


@role_required(Role.MANAGER, Role.CASHIER)
class MyInfoView(View):
    employee_service = EmployeeService()

    def get(self, request):
        employee = self.employee_service.get_by_user_id(request.session["user_id"])
        if not employee:
            raise Http404("No employee profile is linked to your account.")
        fields = [
            ("Surname", employee["empl_surname"]),
            ("Name", employee["empl_name"]),
            ("Patronymic", employee["empl_patronymic"]),
            ("Role", employee["empl_role"]),
            ("Salary", employee["salary"]),
            ("Date of birth", employee["date_of_birth"]),
            ("Date of start", employee["date_of_start"]),
            ("Phone", employee["phone_number"]),
            ("City", employee["city"]),
            ("Street", employee["street"]),
            ("Zip code", employee["zip_code"]),
        ]
        return render(
            request,
            "employees/my_info.html",
            {"employee": employee, "fields": fields},
        )


@role_required(Role.MANAGER)
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


@role_required(Role.MANAGER)
class GetEmployeesView(View):
    employee_service = EmployeeService()

    def get(self, request):
        sort_by, sort_dir = resolve_sort(
            request, EMPLOYEE_SORTABLE, default="empl_surname"
        )
        rows = self.employee_service.get_all(request, sort_by, sort_dir)
        self.employee_service.annotate_deletable(rows)

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
                    "filters": EMPLOYEE_FILTERS,
                    "row_id_key": "id",
                    "actions": [
                        {
                            "label": "Edit",
                            "url_name": "employees:edit-employee",
                            "icon": "fa-solid fa-pen",
                        },
                        {
                            "label": "Delete",
                            "url_name": "employees:delete-employee",
                            "icon": "fa-solid fa-trash",
                            "method": "post",
                            "confirm": "Delete this employee?",
                            "block_key": "delete_block_reason",
                        },
                    ],
                },
            },
        )


@role_required(Role.MANAGER)
class EditEmployeeView(View):
    employee_service = EmployeeService()

    def get(self, request, pk):
        employee = self.employee_service.get_by_id(pk)
        if not employee:
            raise Http404(f"Employee with id {pk} was not found")
        form = EmployeeForm(initial=employee)
        return render(
            request,
            "home.html",
            {
                "form": form,
                "form_title": "Edit Employee",
                "form_action": reverse("employees:edit-employee", args=[pk]),
                "submit_label": "Save",
            },
        )

    def post(self, request, pk):
        form = EmployeeForm(request.POST)
        if form.is_valid():
            self.employee_service.update_employee(pk, form.cleaned_data)
            return redirect("employees:employees")
        return render(
            request,
            "home.html",
            {
                "form": form,
                "form_title": "Edit Employee",
                "form_action": reverse("employees:edit-employee", args=[pk]),
                "submit_label": "Save",
            },
        )


@role_required(Role.MANAGER)
class DeleteEmployeeView(View):
    employee_service = EmployeeService()

    def post(self, request, employee_id):
        try:
            self.employee_service.delete(employee_id)
            return HttpResponse("")
        except ValueError as e:
            return HttpResponse(str(e), status=409)
