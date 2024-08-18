class SeparateSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin'):
            request.session_cookie_name = 'admin_sessionid'
            request.csrf_cookie_name = 'admin_csrftoken'
        else:
            request.session_cookie_name = 'user_sessionid'
            request.csrf_cookie_name = 'user_csrftoken'

        response = self.get_response(request)
        return response