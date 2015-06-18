# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demo_djangosuit', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='is_active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='city',
            name='capital',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fridge',
            name='is_quiet',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='kitchensink',
            name='boolean_with_help',
            field=models.BooleanField(default=False, help_text=b'Boolean field with help text'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='kitchensink',
            name='hidden_checkbox',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='microwave',
            name='is_compact',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
