# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group_discussion', '0016_auto_20150804_1520'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('action', models.CharField(max_length=255)),
                ('details', models.TextField()),
                ('user', models.ForeignKey(related_name='log', to='group_discussion.TopicUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
