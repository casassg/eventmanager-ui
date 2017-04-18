from django.db import models


# Create your models here.


class Event(models.Model):
    name = models.CharField(max_length=240)
    code = models.CharField(primary_key=True, max_length=240)
    query = models.CharField(max_length=500)
    tracking_enabled = models.BooleanField(default=False)

    @staticmethod
    def create(name, query, tracking=False):
        event = Event()
        event.name = name
        event.query = query
        event.code = name.lower().replace(' ', '-')
        event.save(force_insert=True)
