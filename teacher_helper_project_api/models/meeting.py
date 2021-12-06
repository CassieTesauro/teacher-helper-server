from django.db import models
from django.contrib.auth.models import User


class Meeting(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    date = models.DateField() 
    time = models.TimeField() 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
