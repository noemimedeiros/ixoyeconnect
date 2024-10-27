from django import template

register = template.Library()

@register.filter
def instance_name(obj):
    return obj.__class__.__name__
