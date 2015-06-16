# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('group_discussion', '0011_topicuser_group_centrality'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 1, 17, 16, 31, 864411, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='topic',
            name='created_by',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
