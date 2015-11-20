# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group_discussion', '0023_profile_has_seen_contacted'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='thumbnail_url',
            field=models.URLField(null=True),
            preserve_default=True,
        ),
    ]
