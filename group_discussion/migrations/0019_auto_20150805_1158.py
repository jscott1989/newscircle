# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('group_discussion', '0018_auto_20150805_0937'),
    ]

    operations = [
        migrations.AddField(
            model_name='topicuser',
            name='active',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topicuser',
            name='last_interaction',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 5, 11, 58, 49, 851461, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
