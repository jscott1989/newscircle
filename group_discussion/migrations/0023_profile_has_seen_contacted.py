# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group_discussion', '0022_topic_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='has_seen_contacted',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
