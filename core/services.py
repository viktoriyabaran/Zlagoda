from typing import Protocol

from django.contrib.auth.hashers import check_password

from core.repository import get_user_by_username


class IAuthService(Protocol):
    def authenticate(self, username: str, password: str) -> dict | None: ...


class AuthService:
    def authenticate(self, username: str, password: str) -> dict | None:
        user = get_user_by_username(username)
        if user and check_password(password, user["password"]):
            return user
        return None
