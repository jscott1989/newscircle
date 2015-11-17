# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group_discussion', '0021_auto_20151102_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='url',
            field=models.URLField(null=True),
            preserve_default=True,
        ),
    ]
