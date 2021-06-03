
# //custome tags
from django import template


register = template.Library()

@register.simple_tag

def getMessage(percentage):
    
    message = " "
    
    if(percentage >= 90 and percentage != " "):
        message = "Congrtatulations!!! You did really well in exam"
    elif(percentage <90 and percentage>=50 and percentage != " "):
        message = "Ooh it was good but you can do better try again"
    else:
        message = "So sorry it was not good you need more practice!"

    return message

# def isEmpty(percentage):
#     if(percentage == " "):
#         return False
#     else:
#         return True



    
    



