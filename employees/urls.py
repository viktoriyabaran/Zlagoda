from django.urls import path

from .views import AddEmployeeView, GetEmployeesView

app_name = "employees"

urlpatterns = [
    path("", GetEmployeesView.as_view(), name="employees"),
    path("add/", AddEmployeeView.as_view(), name="add-employee"),
]
