from django.shortcuts import redirect

class RestrictAdminUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser and request.path.startswith('/home/'):
                return redirect('adminhome')  # Redirect admin to admin page
            elif not request.user.is_superuser and request.path.startswith('/adminhome/'):
                return redirect('home')  # Redirect normal user to user page

        response = self.get_response(request)
        return response
