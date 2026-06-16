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
from core.table_config import (
    CATEGORY_REVENUE_COLUMNS,
    CATEGORY_REVENUE_SORTABLE,
    TOP_CUSTOMERS_COLUMNS,
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


@role_required(Role.MANAGER)
class CategoryRevenueView(View):
    stats_service: IStatisticsService = StatisticsService()

    def get(self, request):
        sort_by, sort_dir = resolve_sort(
            request, CATEGORY_REVENUE_SORTABLE, default="category_name"
        )
        promotional = {"true": True, "false": False}.get(request.GET.get("promotional"))
        return render(
            request,
            "home.html",
            {
                "list": {
                    "title": "Category Revenue",
                    "subtitle": "Items sold and revenue share by promotional status",
                    "rows": self.stats_service.get_category_revenue(
                        sort_by,
                        sort_dir,
                        promotional=promotional,
                    ),
                    "columns": CATEGORY_REVENUE_COLUMNS,
                    "sort": {"by": sort_by, "dir": sort_dir},
                    "filters": [
                        {
                            "key": "promotional",
                            "label": "Promotional",
                            "type": "select",
                            "options": [
                                {"value": "true", "label": "Promotional"},
                                {"value": "false", "label": "Non-promotional"},
                            ],
                        },
                    ],
                    "empty_message": "Not enough data for statistics.",
                }
            },
        )


@role_required(Role.MANAGER)
class TopCustomersView(View):
    stats_service: IStatisticsService = StatisticsService()

    def get(self, request):
        return render(
            request,
            "home.html",
            {
                "list": {
                    "title": "Top Customers",
                    "subtitle": "Bought all 5 of the most expensive non-promotional products",
                    "rows": self.stats_service.get_top_customers(),
                    "columns": TOP_CUSTOMERS_COLUMNS,
                    "empty_message": "Not enough data for statistics.",
                }
            },
        )
