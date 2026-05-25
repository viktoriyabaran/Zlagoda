from functools import wraps

from django.shortcuts import redirect
from django.views import View


def login_required(view):
    if isinstance(view, type) and issubclass(view, View):
        original_dispatch = view.dispatch

        @wraps(original_dispatch)
        def dispatch_wrapper(self, request, *args, **kwargs):
            if not request.session.get("user_id"):
                return redirect("core:login")
            return original_dispatch(self, request, *args, **kwargs)

        view.dispatch = dispatch_wrapper
        return view

    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("user_id"):
            return redirect("core:login")
        return view(request, *args, **kwargs)

    return wrapper
