# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group_discussion', '0020_auto_20151028_1939'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dislike',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_voted', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('comment', models.ForeignKey(to='group_discussion.Comment')),
                ('user', models.ForeignKey(to='group_discussion.TopicUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_voted', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('comment', models.ForeignKey(to='group_discussion.Comment')),
                ('user', models.ForeignKey(to='group_discussion.TopicUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='comment',
            name='disliked_by',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='liked_by',
        ),
        migrations.AddField(
            model_name='comment',
            name='disliked_by_raw',
            field=models.ManyToManyField(related_name='dislikes', through='group_discussion.Dislike', to='group_discussion.TopicUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='liked_by_raw',
            field=models.ManyToManyField(related_name='likes', through='group_discussion.Like', to='group_discussion.TopicUser'),
            preserve_default=True,
        ),
    ]
