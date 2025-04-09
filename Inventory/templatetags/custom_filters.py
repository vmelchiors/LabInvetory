from django import template

register = template.Library()

@register.filter
def sub(value, arg):
    """Subtrai arg de value"""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return ''
