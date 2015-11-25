from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def external_url(context, name, *params):
    return context['request'].build_absolute_uri(reverse(name, args=params))
