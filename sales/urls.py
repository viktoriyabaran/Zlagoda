from django.urls import path

from .views import GetChecksView, DeleteCheckView

app_name = "sales"

urlpatterns = [
    path("checks/", GetChecksView.as_view(), name="checks"),
    path("checks/<str:check_id>/delete/", DeleteCheckView.as_view(), name="delete-check"),
]
