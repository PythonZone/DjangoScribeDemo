# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Residence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
                ('url', models.URLField(max_length=80)),
                ('description', models.TextField(null=True)),
                ('city', models.CharField(max_length=80)),
                ('images', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TypeDeLogement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VilleMere',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
                ('url', models.URLField(max_length=80)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='residence',
            name='typesDeLogement',
            field=models.ManyToManyField(related_name='_residences', to='demo_scrapy.TypeDeLogement'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='residence',
            name='villeMere',
            field=models.ForeignKey(related_name='_residences', blank=True, to='demo_scrapy.VilleMere', null=True),
            preserve_default=True,
        ),
    ]
