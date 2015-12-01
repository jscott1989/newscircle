# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group_discussion', '0031_notification_email_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='featured',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topic',
            name='hidden',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
