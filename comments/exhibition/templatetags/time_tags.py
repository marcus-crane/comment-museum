from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def hours_only(value, delimiter=','):
    return value.split(delimiter)[0]
hours_only.is_safe = True