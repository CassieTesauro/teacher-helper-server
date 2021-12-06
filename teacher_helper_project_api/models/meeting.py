from django.db import models

class Meeting(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    date = models.DateField() #OR DATETIME?
    time = models.TimeField() #OR DATETIME?
   #userId = 
