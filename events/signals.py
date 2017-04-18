import json

from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver
from kafka import KafkaProducer, SimpleClient

from events import models


@receiver(pre_save, sender=models.Event)
def kakfa_update(sender, instance, **kwargs):
    producer = KafkaProducer(
        bootstrap_servers=settings.KAFKA_SERVERS,
        retries=5,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    try:
        producer.send('events', repr(instance))
    except:
        client = SimpleClient(hosts=settings.KAFKA_SERVERS)
        client.ensure_topic_exists('events')
        client.close()
        producer.send('events', instance.to_dict())
