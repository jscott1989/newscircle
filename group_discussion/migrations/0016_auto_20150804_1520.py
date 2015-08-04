# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group_discussion', '0015_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='embed_html',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topic',
            name='embed_html',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
    ]
