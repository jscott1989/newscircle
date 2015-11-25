# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group_discussion', '0025_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='image',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
