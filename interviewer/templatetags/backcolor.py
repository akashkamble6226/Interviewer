
# //custome tags
from django import template
import random

register = template.Library()

@register.simple_tag




def chooseBackColor():
    backColorNames = [

        'bg-primary',
        'bg-secondary',
        'bg-success',
        'bg-danger',
        'bg-warning',
        'bg-info',
        'bg-dark',

    ]

    

    return random.choice(backColorNames)



