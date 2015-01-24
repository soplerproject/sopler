import re
from django import template
from datetime import date, timedelta

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
  
# Due Date Calculation
@register.filter
def DueDateCalc(value):
    """
    Example:
       {{ item.ItemDueDate|DueDateCalc }}
    """
    if value is not None:
      delta = value - date.today()
      if delta.days == 0:
	  return "Today"
      elif delta.days > 0:
	  return "Upcoming"
      else :
	  return "Overdue"
    else:
  	  pass