
# //custome tags
from django import template
import random
import datetime

register = template.Library()

@register.simple_tag

def getDate():
    return datetime.date.today()


    
    



