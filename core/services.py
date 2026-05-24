from typing import Protocol

from django.contrib.auth.hashers import check_password
from django.http import HttpRequest

from core.repository import get_user_by_username
from core.roles import Role


class IAuthService(Protocol):
    def authenticate(self, username: str, password: str) -> dict | None: ...
    def register_session_user(
        self, request: HttpRequest, user_id: int, user_role: str | None
    ) -> None: ...
    def unregister_session_user(self, request: HttpRequest) -> None: ...


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
