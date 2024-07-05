class IsLoggedIn:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        print(request.user,"--------------")

        # if not request.user.is_authenticated and request.method == 'GET':
        #     ALLOWED_URLS = ['/general/','/report/timesheet']
        #     if request.path in ALLOWED_URLS:
        #         if 'next_url' not in request.session:
        #             request.session['next_url'] = request.get_full_path()

        return response