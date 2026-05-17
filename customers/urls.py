from django.urls import path
from .views import AddCustomerView, GetCustomersView

app_name = 'customers'

urlpatterns = [
    path("", GetCustomersView.as_view(), name="customers"),
    path("add/", AddCustomerView.as_view(), name="add-customer"),
]
