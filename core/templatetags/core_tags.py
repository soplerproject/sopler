from django import template

register = template.Library()

@register.filter
def full_name(user):
    """
    Example:
       {{ user|full_name }}
    """
    return user.get_full_name()