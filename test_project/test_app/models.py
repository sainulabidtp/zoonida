from django.db import models
import shortuuid
# Create your models here.

class ShortenedURL(models.Model):
    original_url = models.URLField()
    short_code = models.CharField(max_length=15,unique=True,default=shortuuid.uuid)
    visits =models.IntegerField(default=0)

    def __str__(self):
        return  self.original_url