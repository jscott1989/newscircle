# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group_discussion', '0005_auto_20150402_1841'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField()),
                ('topic', models.ForeignKey(to='group_discussion.Topic')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='topicuser',
            name='group',
            field=models.ForeignKey(related_name='users', to='group_discussion.Group', null=True),
            preserve_default=True,
        ),
    ]
