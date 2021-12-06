from django.db import models

class StudentMeeting(models.model):
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    meeting = models.ForeignKey("Meeting", on_delete=models.CASCADE)