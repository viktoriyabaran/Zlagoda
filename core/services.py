from typing import Protocol

from django.contrib.auth.hashers import check_password
from django.http import HttpRequest

from core.query_helpers import order_by_sql
from core.repository import get_user_by_username
from core.roles import Role
from customers.repository import get_top_customers
from sales.repository import get_category_revenue_stats


class IAuthService(Protocol):
    def authenticate(self, username: str, password: str) -> dict | None: ...
    def register_session_user(
        self, request: HttpRequest, user_id: int, user_role: str | None
    ) -> None: ...
    def unregister_session_user(self, request: HttpRequest) -> None: ...


class IStatisticsService(Protocol):
    def get_category_revenue(self, sort_by: str, sort_dir: str) -> list[dict]: ...
    def get_top_customers(self) -> list[dict]: ...


class AuthService:
    def authenticate(self, username: str, password: str) -> dict | None:
        user = get_user_by_username(username)
        if user and check_password(password, user["password"]):
            return user
        return None

    def register_session_user(
        self, request: HttpRequest, user_id: int, user_role: str | None
    ) -> None:
        request.session.cycle_key()
        request.session["user_id"] = user_id
        request.session["user_role"] = user_role if user_role in Role.ALL else None

    def unregister_session_user(self, request: HttpRequest) -> None:
        request.session.flush()


class StatisticsService:
    def get_category_revenue(self, sort_by: str, sort_dir: str) -> list[dict]:
        return get_category_revenue_stats(order_by_sql(sort_by, sort_dir))

    def get_top_customers(self) -> list[dict]:
        return get_top_customers()
