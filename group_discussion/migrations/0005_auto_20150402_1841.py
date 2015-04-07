# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('group_discussion', '0004_topicuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(related_name='comments', to='group_discussion.TopicUser'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='topicuser',
            name='user',
            field=models.ForeignKey(related_name='topic_users', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
