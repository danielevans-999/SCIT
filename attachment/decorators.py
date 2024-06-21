from functools import wraps
from django.shortcuts import redirect

def prevent_login_access(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('summary')  # Redirect to the home page if already logged in
        return view_func(request, *args, **kwargs)
    return wrapper


def prevent_admin_login_access(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            current_url = request.session.get('next')
            return redirect(current_url)
        return view_func(request, *args, **kwargs)
    return wrapper


def user_is_student(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_student:
            # Redirect to a login page or an access denied page
            return redirect('login')  # Change 'login' to your login URL or access denied page

        return view_func(request, *args, **kwargs)

    return _wrapped_view
