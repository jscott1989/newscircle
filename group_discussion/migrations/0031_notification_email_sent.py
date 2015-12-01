# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group_discussion', '0030_auto_20151201_1306'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='email_sent',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
