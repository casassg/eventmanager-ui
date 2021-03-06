# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-18 21:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('name', models.CharField(max_length=240)),
                ('code', models.CharField(max_length=240, primary_key=True, serialize=False)),
                ('query', models.CharField(max_length=500)),
                ('tracking_enabled', models.BooleanField(default=False)),
            ],
        ),
    ]
