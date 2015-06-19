# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PublishableModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=42)),
                ('state', django_fsm.FSMField(default=b'draft', protected=True, max_length=50, verbose_name=b'Publication State', choices=[(b'draft', b'draft'), (b'approved', b'approved'), (b'published', b'published'), (b'expired', b'expired'), (b'deleted', b'deleted')])),
                ('display_from', models.DateTimeField(null=True, blank=True)),
                ('display_until', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
            },
            bases=(models.Model,),
        ),
    ]
