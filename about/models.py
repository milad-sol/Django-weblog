from django.db import models


# Create your models here.
class About(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()

    our_vision_title = models.CharField(max_length=100)
    our_vision_body = models.TextField()
    what_we_offer = models.TextField()

    def __str__(self):
        return self.title
