from django.shortcuts import redirect, render
from django.views import View

from core.query_helpers import resolve_sort
from core.roles import Role
from core.services import (
    AuthService,
    IAuthService,
    IStatisticsService,
    StatisticsService,
)

from .decorators import role_required
from .forms import UserLoginForm


class LoginView(View):
    auth_service: IAuthService = AuthService()

    def get(self, request):
        form = UserLoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = self.auth_service.authenticate(
                form.cleaned_data["username"],
                form.cleaned_data["password"],
            )
            if user:
                self.auth_service.register_session_user(
                    request, user["id"], user.get("empl_role")
                )
                return redirect("core:home")
            form.add_error(None, "Invalid credentials")
        return render(request, "login.html", {"form": form})


class LogoutView(View):
    auth_service: IAuthService = AuthService()

    def post(self, request):
        self.auth_service.unregister_session_user(request)
        return redirect("core:login")


@role_required(Role.MANAGER, Role.CASHIER)
def home(request):
    return render(request, "home.html")


PRODUCT_STATS_COLUMNS = [
    {"key": "category_name", "label": "Category", "sortable": True},
    {"key": "promotional_product", "label": "Promo?", "sortable": True},
    {"key": "total_units", "label": "Total Units", "sortable": False},
    {"key": "total_revenue", "label": "Total Revenue", "sortable": False},
    {"key": "percent_of_category_revenue", "label": "Percent", "sortable": False},
]
PRODUCT_STATS_SORTABLE = {c["key"] for c in PRODUCT_STATS_COLUMNS if c["sortable"]}


@role_required(Role.MANAGER)
class GetProductsStatisticsView(View):
    stats_service: IStatisticsService = StatisticsService()

    def get(self, request):
        sort_by, sort_dir = resolve_sort(
            request, PRODUCT_STATS_SORTABLE, default="category_name"
        )
        data = self.stats_service.get_product_per_category_stats(sort_by, sort_dir)

        return render(
            request,
            "home.html",
            {
                "list": {
                    "title": "Products per category",
                    "subtitle": "Some stats",
                    "rows": data,
                    "columns": PRODUCT_STATS_COLUMNS,
                    "sort": {"by": sort_by, "dir": sort_dir},
                    "empty_message": "Not enough data for statistics.",
                    "row_id_key": "category_name",
                }
            },
        )


@role_required(Role.MANAGER)
class GetCustomersStatisticsView(View):
    stats_service: IStatisticsService = StatisticsService()

    def get(self, request):
        data = self.stats_service.get_richest_customers_stats()

        return render(
            request,
            "home.html",
            {
                "list": {
                    "title": "Customers who have bought fie most expensive non-promo products",
                    "subtitle": "Some stats",
                    "rows": data,
                    "columns": [
                        {
                            "key": "cust_surname",
                            "label": "Surname",
                            "sortable": False,
                        },
                        {
                            "key": "cust_name",
                            "label": "Surname",
                            "sortable": False,
                        },
                        {
                            "key": "phone_number",
                            "label": "Phone Number",
                            "sortable": False,
                        },
                        {
                            "key": "percent",
                            "label": "Discount Percent",
                            "sortable": False,
                        },
                    ],
                    "empty_message": "Not enough data for statistics.",
                    "row_id_key": "cust_surname",
                }
            },
        )
