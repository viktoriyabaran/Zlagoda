from django.shortcuts import redirect, render
from django.views import View

from core.services import AuthService, IAuthService

from .decorators import login_required
from .forms import UserForm


class LoginView(View):
    auth_service: IAuthService = AuthService()

    def get(self, request):
        form = UserForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            user = self.auth_service.authenticate(
                form.cleaned_data["username"],
                form.cleaned_data["password"],
            )
            if user:
                self.auth_service.register_session_user(request, user["id"])
                return redirect("core:home")
            form.add_error(None, "Invalid credentials")
        return render(request, "login.html", {"form": form})


class LogoutView(View):
    auth_service: IAuthService = AuthService()

    def post(self, request):
        self.auth_service.unregister_session_user(request)
        return redirect("core:login")


@login_required
def home(request):
    return render(request, "home.html")
