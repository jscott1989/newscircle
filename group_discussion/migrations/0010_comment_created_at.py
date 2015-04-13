# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('group_discussion', '0009_auto_20150409_1214'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 9, 12, 57, 2, 759549)),
            preserve_default=False,
        ),
    ]
