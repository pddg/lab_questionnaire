from django.db import models


class StudyOffice(models.Model):
    name = models.CharField(max_length=128, unique=True)
    capacity = models.IntegerField(default=0)
