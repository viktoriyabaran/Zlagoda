from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        "id_employee",
        "empl_surname",
        "empl_name",
        "empl_role",
    ]
    search_fields = [
        "empl_surname",
        "empl_name",
    ]
    list_filter = [
        "empl_role",
    ]
