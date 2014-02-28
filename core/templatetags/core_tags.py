import re
from django import template

register = template.Library()


# Return get_full_name()
@register.filter
def full_name(user):
    """
    Example:
       {{ user|full_name }}
    """
    return user.get_full_name()


# Regular Expression Replace Template Filter
@register.filter
def replace ( string, args ): 
    search  = args.split(args[0])[1]
    replace = args.split(args[0])[2]

    return re.sub( search, replace, string )