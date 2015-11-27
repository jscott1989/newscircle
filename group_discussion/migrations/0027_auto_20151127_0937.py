# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group_discussion', '0026_notification_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='url',
            field=models.URLField(max_length=3000, null=True),
            preserve_default=True,
        ),
    ]
