from django.template import Library

register = Library()

@register.filter
def split(value):
    delimiter = '/'
    return value.split(delimiter)

@register.filter
def to_str(value):
    """converts int to string"""
    return str(value)