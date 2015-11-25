from django.shortcuts import redirect

class ConsentMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated():
            if not request.user.profile.given_consent:
                if not request.path.startswith("/consent") and\
                        not request.path.startswith("/info"):
                    return redirect("/consent?next=" + request.path)
        return None

class NoWWWRedirectMiddleware(object):
    def process_request(self, request):
        if request.method == 'GET':  # if wanna be a prefect REST citizen, consider HEAD and OPTIONS here as well
            host = request.get_host()
            if host.lower().find('www.') == 0:
                no_www_host = host[4:]
                url = request.build_absolute_uri().replace(host, no_www_host, 1)
                return redirect(url)
