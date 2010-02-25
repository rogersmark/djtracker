from django import template
from django.template.defaultfilters import stringfilter

from djtracker.models import ISSUE_ATTRIBUTES

register = template.Library()

@register.filter
@stringfilter
def transattr(value):
    """ translate an attribute name """
    return ISSUE_ATTRIBUTES[value] if value in ISSUE_ATTRIBUTES else value