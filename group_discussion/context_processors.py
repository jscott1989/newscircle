""" Context Processors. """

from django.conf import settings as django_settings


def settings(request):
    """ Add useful settings into context. """
    return {
        "ALLOW_AUTHENTICATION": django_settings.ALLOW_AUTHENTICATION
    }
