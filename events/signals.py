import json
import logging
from functools import reduce

from django import dispatch
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
refresh_arch_signal = dispatch.Signal()

@receiver(pre_save, sender=models.Event)
def kakfa_check(sender, instance, **kwargs):
    message = create_message(TEST_TYPE, 'ignore')
    logging.info('Checking connexion...')
    send_to_kafka(message)


@receiver(post_save, sender=models.Event)
def kakfa_event_update(sender, instance, **kwargs):
    message = create_message(EVENT_TYPE, 'update', instance.to_dict())
    send_to_kafka(message)


@receiver(post_save, sender=models.Event)
def kakfa_tokens_update(sender, instance, **kwargs):
    active = models.ActiveTokens.objects.first()
    new_tokens = get_new_keywords()
    if active.tokens == new_tokens:
        return
    active.tokens = new_tokens
    active.save()
    message = create_message(QUERIES_TYPE, 'update', new_tokens)
    send_to_kafka(message)


@receiver(refresh_arch_signal)
def refresh_arch(sender, **kwargs):
    active = models.ActiveTokens.objects.first()
    message = create_message(QUERIES_TYPE, 'update', active)
    send_to_kafka(message)
    for instance in models.Event.objects.all():
        message = create_message(EVENT_TYPE, 'update', instance.to_dict())
        send_to_kafka(message)


def send_to_kafka(message):
    producer = get_producer()
    try:
        producer.send(settings.KAFKA_TOPIC, message)
    except:
        client = SimpleClient(hosts=settings.KAFKA_SERVERS)
        client.ensure_topic_exists(settings.KAFKA_TOPIC)
        client.close()
        producer.send(settings.KAFKA_TOPIC, message)
    producer.close(10)


def create_message(type, action, data=None):
    return {
        'type': type,
        'action': action,
        'data': data
    }


def get_producer():
    producer = KafkaProducer(
        bootstrap_servers=settings.KAFKA_SERVERS,
        retries=5,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    return producer


def get_new_keywords():
    tokens = map(lambda x: x['tokens'].lower().split(','), models.Event.objects.values('tokens'))
    return list(set(reduce(lambda x, y: x + y, tokens)))
