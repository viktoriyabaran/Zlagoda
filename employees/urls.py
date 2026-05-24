from django.urls import path

from .views import AddEmployeeView, EditEmployeeView, GetEmployeesView, DeleteEmployeeView

app_name = "employees"

urlpatterns = [
    path("", GetEmployeesView.as_view(), name="employees"),
    path("add/", AddEmployeeView.as_view(), name="add-employee"),
    path("<int:pk>/edit/", EditEmployeeView.as_view(), name="edit-employee"),
    path("<int:employee_id>/delete/", DeleteEmployeeView.as_view(), name="delete-employee"),
]
