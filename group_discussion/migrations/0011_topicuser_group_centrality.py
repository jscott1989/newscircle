# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group_discussion', '0010_comment_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='topicuser',
            name='group_centrality',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
