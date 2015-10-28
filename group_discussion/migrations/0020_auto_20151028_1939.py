# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group_discussion', '0019_auto_20150805_1158'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='can_be_contacted',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='given_consent',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
