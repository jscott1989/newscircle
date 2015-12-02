""" Context Processors. """

from django.conf import settings as django_settings
from serializers import NotificationSerializer
from rest_framework.renderers import JSONRenderer
from django.utils.encoding import smart_text


def settings(request):
    """ Add useful settings into context. """
    return {
        "ALLOW_AUTHENTICATION": django_settings.ALLOW_AUTHENTICATION
    }

def notifications(request):
    if not request.user.is_authenticated():
        return {"notifications": []}
    r = JSONRenderer()

    def clean_unicode(p):
        p["image"] = smart_text(p["image"])
        p["short"] = smart_text(p["short"])
        p["html"] = smart_text(p["html"])
        return p


    rr = [clean_unicode(NotificationSerializer(n).data)
                                   for n in request.user.notifications.all()]
    return {
        "notifications": r.render(rr)
    }