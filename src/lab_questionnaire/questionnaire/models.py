from django.db import models


class StudyOffice(models.Model):
    number = models.IntegerField(unique=False, default=0, verbose_name=u"番号")
    name = models.CharField(max_length=128, unique=True)
    supervisor = models.CharField(max_length=128, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    capacity = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['number']
        verbose_name = u"研究室"
