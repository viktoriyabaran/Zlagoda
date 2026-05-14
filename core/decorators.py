from functools import wraps

from django.shortcuts import redirect


def login_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("user_id"):
            return redirect("core:login")
        return view(request, *args, **kwargs)

    return wrapper
