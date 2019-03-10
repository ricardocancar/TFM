from django.db import models

# Create your models here.
class PoliticalClasification(models.Model):
    political = models.CharField(max_length=250)
    content = models.CharField(max_length=250)
    numbers = models.DecimalField(decimal_places=13, max_digits=100)