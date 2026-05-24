from django.urls import path

from .views import AddCustomerView, EditCustomerView, GetCustomersView, DeleteCustomerView

app_name = "customers"

urlpatterns = [
    path("", GetCustomersView.as_view(), name="customers"),
    path("add/", AddCustomerView.as_view(), name="add-customer"),
    path(
        "<int:customer_card_id>/edit/", EditCustomerView.as_view(), name="edit-customer"
    ),
    path("<int:customer_id>/delete/", DeleteCustomerView.as_view(), name="delete-customer"),
]
