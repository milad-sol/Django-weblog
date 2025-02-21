from django.db import models


# Create your models here.
class WeblogSettings(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    footer = models.CharField(max_length=255)
    description = models.TextField()
    keywords = models.TextField()
    author = models.CharField(max_length=255)
    og_title = models.CharField(max_length=255)
    og_description = models.TextField()
    og_url = models.CharField(max_length=255)

    def __str__(self):
        return self.title
