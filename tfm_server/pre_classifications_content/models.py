from django.db import models

# Create your models here.
class PreClassificationsContent(models.Model):
    video_name = models.CharField(max_length=250)
    start_end = models.CharField(max_length=250)
    label = models.CharField(max_length=80)
    text = models.TextField(blank=True, null=True)
