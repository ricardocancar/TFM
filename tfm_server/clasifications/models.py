from django.db import models

# Create your models here.
class Clasifications(models.Model):
    video_name = models.CharField(max_length=250)
    path = models.CharField(max_length=250)
    label = models.CharField(max_length=80)
    score = models.DecimalField(decimal_places=13, max_digits=100)