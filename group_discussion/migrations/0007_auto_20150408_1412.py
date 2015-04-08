# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group_discussion', '0006_auto_20150407_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='locked',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='topicuser',
            name='topic',
            field=models.ForeignKey(related_name='users', to='group_discussion.Topic'),
            preserve_default=True,
        ),
    ]
