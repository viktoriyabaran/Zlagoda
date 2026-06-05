from django.urls import path

from .views import (
    AddItemToCheckView,
    ApplyCardView,
    CreateCheckView,
    DeleteCheckView,
    FinalizeCheckView,
    GetCheckDetailView,
    GetChecksView,
)

app_name = "sales"

urlpatterns = [
    path("checks/", GetChecksView.as_view(), name="checks"),
    path("checks/<int:check_id>/", GetCheckDetailView.as_view(), name="check-detail"),
    path(
        "checks/<str:check_id>/delete/", DeleteCheckView.as_view(), name="delete-check"
    ),
    path("checks/create/", CreateCheckView.as_view(), name="create-check"),
    path("checks/add-item/", AddItemToCheckView.as_view(), name="add-item"),
    path("checks/apply-card/", ApplyCardView.as_view(), name="apply-card"),
    path("checks/finalize/", FinalizeCheckView.as_view(), name="finalize-check"),
]
