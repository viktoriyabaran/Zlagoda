from django.urls import path
from .views import AddCustomerView, GetCustomersView

app_name = 'customers'

urlpatterns = [
    path("customers/", GetCustomersView.as_view(), name="customers"),
    path("customers/add/", AddCustomerView.as_view(), name="add-customer"),
]
