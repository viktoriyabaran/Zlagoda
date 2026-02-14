from django.urls import path

from .views import LoginView, home

app_name = "core"

urlpatterns = [
    path("home/", home, name="home"),
    path("login/", LoginView.as_view(), name="login"),
]
