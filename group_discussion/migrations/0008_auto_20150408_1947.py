# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group_discussion', '0007_auto_20150408_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='disliked_by',
            field=models.ManyToManyField(related_name='dislikes', to='group_discussion.TopicUser'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comment',
            name='liked_by',
            field=models.ManyToManyField(related_name='likes', to='group_discussion.TopicUser'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='group',
            name='topic',
            field=models.ForeignKey(related_name='groups', to='group_discussion.Topic'),
            preserve_default=True,
        ),
    ]
