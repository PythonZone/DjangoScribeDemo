# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cyberhotel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bedroom',
            name='nbOfDoubleBeds',
            field=models.IntegerField(default=0, verbose_name=b'number of double beds'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='residence',
            name='category',
            field=models.CharField(max_length=8, choices=[(b'economy', 'Economy'), (b'standard', 'Standard'), (b'premium', 'Premium'), (b'prestige', 'Prestige')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='residence',
            name='floorMax',
            field=models.IntegerField(verbose_name=b'floor maximum'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='residence',
            name='floorMin',
            field=models.IntegerField(default=0, verbose_name=b'floor minimum'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resident',
            name='gender',
            field=models.CharField(max_length=5, choices=[(b'male', 'Male'), (b'female', 'Female')]),
            preserve_default=True,
        ),
    ]
