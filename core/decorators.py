from functools import wraps

from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.views import View


def _guard(view, roles):
    """Back all role decorators: require login, then check role membership."""

    def denied_response(request):
        if not request.session.get("user_id"):
            return redirect("core:login")
        if request.session.get("user_role") not in roles:
            return HttpResponseForbidden(
                "Viewing this resource is not allowed for you."
            )
        return None

    if isinstance(view, type) and issubclass(view, View):
        original_dispatch = view.dispatch

        @wraps(original_dispatch)
        def dispatch_wrapper(self, request, *args, **kwargs):
            denied = denied_response(request)
            if denied is not None:
                return denied
            return original_dispatch(self, request, *args, **kwargs)

        view.dispatch = dispatch_wrapper
        return view

    @wraps(view)
    def wrapper(request, *args, **kwargs):
        denied = denied_response(request)
        if denied is not None:
            return denied
        return view(request, *args, **kwargs)

    return wrapper


def role_required(*roles):
    return lambda view: _guard(view, frozenset(roles))
