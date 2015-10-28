from django.shortcuts import redirect

class ConsentMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated():
            if not request.user.profile.given_consent:
                if not request.path.startswith("/consent") and\
                        not request.path.startswith("/info"):
                    return redirect("/consent?next=" + request.path)
        return None
