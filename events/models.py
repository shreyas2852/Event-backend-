from django.db import models
from django.core.files.storage import FileSystemStorage



class Event(models.Model):
    name = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100, default='null')
    banner_image_url = models.URLField(default="https://images.google.com/")
