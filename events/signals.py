import json
from functools import reduce

from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from kafka import KafkaProducer, SimpleClient

from events import models

TEST_TYPE = 'test'
EVENT_TYPE = 'event'
QUERIES_TYPE = 'queries'

UPDATE_ACTION = 'update'
IGNORE_ACTION = 'ignore'


def create_message(type, action, data=None):
    return {
        'type': type,
        'action': action,
        'data': data
    }


@receiver(pre_save, sender=models.Event)
def kakfa_check(sender, instance, **kwargs):
    producer = KafkaProducer(
        bootstrap_servers=settings.KAFKA_SERVERS,
        retries=5,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    message = create_message(TEST_TYPE, 'ignore')
    try:
        producer.send('events', message)
    except:
        client = SimpleClient(hosts=settings.KAFKA_SERVERS)
        client.ensure_topic_exists(settings.KAFKA_TOPIC)
        client.close()
        producer.send(settings.KAFKA_TOPIC, message)


@receiver(post_save, sender=models.Event)
def kakfa_event_update(sender, instance, **kwargs):
    producer = KafkaProducer(
        bootstrap_servers=settings.KAFKA_SERVERS,
        retries=5,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    message = create_message(EVENT_TYPE, 'update', instance.to_dict())
    try:
        producer.send(settings.KAFKA_TOPIC, message)
    except:
        client = SimpleClient(hosts=settings.KAFKA_SERVERS)
        client.ensure_topic_exists(settings.KAFKA_TOPIC)
        client.close()
        producer.send(settings.KAFKA_TOPIC, message)


@receiver(post_save, sender=models.Event)
def kakfa_queries_check(sender, instance, **kwargs):
    producer = KafkaProducer(
        bootstrap_servers=settings.KAFKA_SERVERS,
        retries=5,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    query = models.TwitterOutQuery.objects.first()
    new_keywords = get_new_keywords()
    if query.queries == new_keywords:
        return
    query.queries = new_keywords
    query.save()
    message = create_message(QUERIES_TYPE, 'update', new_keywords)
    try:
        producer.send(settings.KAFKA_TOPIC, message)
    except:
        client = SimpleClient(hosts=settings.KAFKA_SERVERS)
        client.ensure_topic_exists(settings.KAFKA_TOPIC)
        client.close()
        producer.send(settings.KAFKA_TOPIC, message)


def get_new_keywords():
    queries = map(lambda x: x['query'].lower().split(','), models.Event.objects.values('query'))
    return list(set(reduce(lambda x, y: x + y, queries)))
