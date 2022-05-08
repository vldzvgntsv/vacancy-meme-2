from django import template

register = template.Library()


@register.filter
def to_circle(value, arg):
    return value.replace(arg, ' •')
