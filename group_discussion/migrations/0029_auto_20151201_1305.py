# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group_discussion', '0028_auto_20151201_1220'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='featured_topics_notification',
            new_name='notifications',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='reply_to_comments_notification',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='reply_to_topics_notification',
        ),
    ]
