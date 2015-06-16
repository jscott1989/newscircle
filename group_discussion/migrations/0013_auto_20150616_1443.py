# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group_discussion', '0012_auto_20150601_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='last_post',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topic',
            name='pinned',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
