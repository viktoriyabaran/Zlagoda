from django.urls import path

from .views import (
    CategoryRevenueView,
    LoginView,
    LogoutView,
    TopCustomersView,
    home,
)

app_name = "core"

urlpatterns = [
    path("home/", home, name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "stats/category-revenue/",
        CategoryRevenueView.as_view(),
        name="category-revenue",
    ),
    path("stats/top-customers/", TopCustomersView.as_view(), name="top-customers"),
]
