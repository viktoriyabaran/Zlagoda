from django.urls import path

from .views import (
    AddEmployeeView,
    DeleteEmployeeView,
    EditEmployeeView,
    GetEmployeesView,
    MyInfoView,
)

app_name = "employees"

urlpatterns = [
    path("", GetEmployeesView.as_view(), name="employees"),
    path("me/", MyInfoView.as_view(), name="my-info"),
    path("add/", AddEmployeeView.as_view(), name="add-employee"),
    path("<int:pk>/edit/", EditEmployeeView.as_view(), name="edit-employee"),
    path("<int:employee_id>/delete/", DeleteEmployeeView.as_view(), name="delete-employee"),
]
