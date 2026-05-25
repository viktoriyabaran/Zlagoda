from django.urls import path

from .views import GetChecksView

app_name = "sales"

urlpatterns = [
    path("checks/", GetChecksView.as_view(), name="checks"),
]
