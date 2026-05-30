from django.shortcuts import redirect, render
from django.views import View

from core.roles import Role
from core.services import AuthService, IAuthService

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
