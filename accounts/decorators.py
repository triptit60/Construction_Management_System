from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def role_required(allowed_roles):
    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect('login')

            try:
                role = request.user.profile.role
            except request.user.profile.RelatedObjectDoesNotExist:
                messages.error(request, "User profile not found.")
                return redirect('dashboard')

            if role not in allowed_roles:
                messages.error(
                    request,
                    "You don't have permission to access this page."
                )
                return redirect('dashboard')

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator