from django.urls import path

from . import views

app_name = "statistics"

urlpatterns = [
    path(
        "statistics/customer-purchases/",
        views.customer_purchase_stats,
        name="customer-purchases",
    ),
    path(
        "statistics/cashiers-all-customers/",
        views.cashiers_served_all_customers,
        name="cashiers-all-customers",
    ),
]
