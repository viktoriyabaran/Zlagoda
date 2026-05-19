from django.urls import path

from .views import AddEmployeeView

app_name = "employees"

urlpatterns = [
    path("add/", AddEmployeeView.as_view(), name="add-employee"),
]
