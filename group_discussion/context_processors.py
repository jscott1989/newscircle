""" Context Processors. """

from django.conf import settings as django_settings
from serializers import NotificationSerializer
from rest_framework.renderers import JSONRenderer


def settings(request):
    """ Add useful settings into context. """
    return {
        "ALLOW_AUTHENTICATION": django_settings.ALLOW_AUTHENTICATION
    }

def notifications(request):
    if not request.user.is_authenticated():
        return {}
    r = JSONRenderer()
    return {
        "notifications": r.render([NotificationSerializer(n).data
                                   for n in request.user.notifications.all()])
    }