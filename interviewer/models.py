from collections import defaultdict
from django.db import models

# Create your models here.



class InterviewData(models.Model):
    questions =  models.CharField(max_length=100)
    answers =  models.TextField()
    given_answer = models.TextField()
    index_no = models.IntegerField()
    accuracy_hundred = models.JSONField(blank=True, null=True)
    accuracy_eighty = models.JSONField(blank=True, null=True)
    accuracy_eighty_words = models.JSONField(blank=True, null=True)
    accuracy_hundred_words = models.JSONField(blank=True, null=True)
    accuracy_zero_words = models.JSONField(blank=True, null=True)
    marks_in_perc = models.IntegerField()

   
    
   
    

    
        


    
