from django.db import models

# Create your models here.


class ClasificationsContent(models.Model):
    video_name = models.CharField(max_length=250)
    start_end = models.CharField(max_length=250)
    label = models.CharField(max_length=80)
    text = models.TextField(blank=True, null=True)
    tag = models.CharField(max_length=250)
    human_term = models.CharField(max_length=250)
    others_tags = models.CharField(max_length=250)
