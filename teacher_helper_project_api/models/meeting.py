from django.db import models

class Meeting(models.Model):
    name = models.Charfield(max_length=50)
    description = models.Charfield(max_length=1000)
    date = models.DateField() #OR DATETIME?
    time = models.TimeField() #OR DATETIME?
    userId = models. #NO 1 TO 1 WITH USER, WHAT TO PUT IN MODEL?
