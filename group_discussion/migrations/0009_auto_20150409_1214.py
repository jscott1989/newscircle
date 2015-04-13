# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('group_discussion', '0008_auto_20150408_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topicuser',
            name='group',
            field=models.ForeignKey(related_name='users', on_delete=django.db.models.deletion.SET_NULL, to='group_discussion.Group', null=True),
            preserve_default=True,
        ),
    ]
