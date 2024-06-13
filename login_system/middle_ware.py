from django.shortcuts import redirect

class RestrictAdminUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser and request.path.startswith('/user/'):
                return redirect('adminhome')  # Redirect admin to admin page
            elif not request.user.is_superuser and request.path.startswith('/admin/'):
                return redirect('userhome')  # Redirect normal user to user page

        response = self.get_response(request)
        return response
