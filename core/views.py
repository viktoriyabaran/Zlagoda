from django.shortcuts import redirect, render
from django.views import View

from core.services import AuthService, IAuthService

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
                request.session["user_id"] = user["id"]
                return redirect("core:home")
            form.add_error(None, "Invalid credentials")
        return render(request, "login.html", {"form": form})


def home(request):
    return render(request, "home.html")
