from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Ko'paytirish filteri"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def div(value, arg):
    """Bo'lish filteri"""
    try:
        if float(arg) == 0:
            return 0
        return float(value) / float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def sub(value, arg):
    """Ayirish filteri"""
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return 0
