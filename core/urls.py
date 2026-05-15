from django.urls import path

from .views import LoginView, LogoutView, home

app_name = "core"

urlpatterns = [
    path("home/", home, name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
