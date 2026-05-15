from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
    path("", RedirectView.as_view(pattern_name="core:home", permanent=False)),
    path("", include("core.urls")),
    path("employees/", include("employees.urls")),
    path("products/", include("products.urls")),
    path("sales/", include("sales.urls")),
    path("customers/", include("customers.urls")),
]
