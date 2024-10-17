from datetime import date
from django import template

register = template.Library()

@register.filter
def evento_passado(data):
    return date.today() > data