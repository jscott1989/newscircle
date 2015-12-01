# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group_discussion', '0029_auto_20151201_1305'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='notifications',
            new_name='notifications_setting',
        ),
    ]
