from django.db import models


# Create your models here.


class Event(models.Model):
    name = models.CharField(max_length=240)
    code = models.CharField(primary_key=True, max_length=240)
    tokens = models.CharField(max_length=500)
    tracking_enabled = models.BooleanField(default=False)

    @staticmethod
    def create(name, tokens, tracking=False):
        event = Event()
        event.name = name
        event.tokens = tokens
        event.code = name.lower().replace(' ', '-').replace('_', '-')
        event.save(force_insert=True)
        return event

    def to_dict(self):
        return {'code': self.code, 'tokens': self.tokens, 'tracking': str(self.tracking_enabled)}


class ActiveTokens(models.Model):
    tokens = models.CharField(max_length=5000)
