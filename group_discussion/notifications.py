"""Notifications."""
from django.template.loader import render_to_string
from django.template import RequestContext
from models import Notification


def notify(request, user, notification_type, data):
    """Send a notification to a user."""
    content = render_to_string(
        "notifications/%s.html" % notification_type,
        data,
        context_instance=RequestContext(request))

    subject = content.split("<notification_subject>")[1]\
        .split("</notification_subject>")[0]
    html = content.split("<notification_html>")[1]\
        .split("</notification_html>")[0]
    text = content.split("<notification_text>")[1]\
        .split("</notification_text>")[0]
    image = content.split("<notification_image>")[1]\
        .split("</notification_image>")[0]

    Notification(user=user,
                 subject=subject,
                 html=html,
                 text=text,
                 image=image).save()
    # TODO: Send email