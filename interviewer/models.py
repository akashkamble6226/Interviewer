from django.db import models

# Create your models here.

# is equal to is mandatory

class InterviewData(models.Model):
    questions =  models.CharField(max_length=100)
    answers =  models.TextField()
    given_answer = models.TextField()
    index_no = models.IntegerField()
    accuracy_hundred = models.JSONField(blank=True, null=True)
    accuracy_eighty = models.JSONField(blank=True, null=True)
   
    

    
        


    
