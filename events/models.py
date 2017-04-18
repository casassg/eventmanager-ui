from django.db import models

# Create your models here.


class Events(models.Model):
    name = models.CharField(max_length=240)
    code = models.CharField(primary_key=True, max_length=240)
    query = models.CharField(max_length=500)
    tracking_enabled = models.BooleanField(default=False)
