from django import template

register = template.Library()


@register.filter
def is_string(value):
    return isinstance(value, str)


@register.filter
def addstr(arg1, arg2):
    return str(arg1) + str(arg2)
