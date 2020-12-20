from django.db import models


# Create your models here.
class Movie(models.Model):
    name = models.CharField(max_length=128)
    star = models.IntegerField(default=0)
    comment = models.TextField()
