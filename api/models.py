__author__ = 'Duy'

from django.db import models
from django.utils import timezone

class portal(models.Model):
    app_label = 'api'
    Name = models.CharField(max_length=200)
    Resource = models.CharField(max_length=10)
    Link = models.URLField(max_length=200)
    def ___str___(self):
        return self.Name

    def getLink(self):
        return self.Link

    def getResource(self):
        return self.Resource
