from typing import Protocol

from django.contrib.auth.hashers import check_password
from django.http import HttpRequest

from core.repository import get_user_by_username
from core.roles import Role
from customers.repository import get_richest_customers
from sales.repository import get_per_category_stat


class IAuthService(Protocol):
    def authenticate(self, username: str, password: str) -> dict | None: ...
    def register_session_user(
        self, request: HttpRequest, user_id: int, user_role: str | None
    ) -> None: ...
    def unregister_session_user(self, request: HttpRequest) -> None: ...


class IStatisticsService(Protocol):
    def get_product_per_category_stats(self) -> list[dict]: ...
    def get_richest_customers_stats(self) -> list[dict]: ...


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
    def get_product_per_category_stats(self) -> list[dict]:
        return get_per_category_stat()

    def get_richest_customers_stats(self) -> list[dict]:
        return get_richest_customers()
