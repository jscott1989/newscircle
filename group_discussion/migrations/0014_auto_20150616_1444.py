# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('group_discussion', '0013_auto_20150616_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='last_post',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 16, 14, 44, 28, 217819, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
