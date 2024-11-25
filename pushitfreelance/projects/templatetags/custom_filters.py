from django import template

register = template.Library()


@register.filter(name='multiply')
def multiply(value, arg):
    """Умножает значение на аргумент."""
    return value * arg
