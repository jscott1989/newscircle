# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group_discussion', '0027_auto_20151127_0937'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='featured_topics_notification',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='reply_to_comments_notification',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='reply_to_topics_notification',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
