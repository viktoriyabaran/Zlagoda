from django.urls import path

from .views import (
    GetCustomersStatisticsView,
    GetProductsStatisticsView,
    LoginView,
    LogoutView,
    home,
)

app_name = "core"

urlpatterns = [
    path("home/", home, name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("product-stats/", GetProductsStatisticsView.as_view(), name="product-stats"),
    path(
        "customer-stats/", GetCustomersStatisticsView.as_view(), name="customer-stats"
    ),
]
