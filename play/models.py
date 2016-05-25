from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible
class PlayApp(models.Model):
    app_id = models.CharField(max_length=256)
    app_name = models.CharField(max_length=256)
    dev_name = models.CharField(max_length=256)
    dev_email = models.EmailField()
    icon_url = models.URLField()

    def __str__(self):
        return self.app_name

