# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'computed_fields': ['employees_company', 'departments'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('company', models.ForeignKey(related_name='_compartments', to='companies101rdb.Company')),
            ],
            options={
                'computed_fields': ['employees_department'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('salary', models.FloatField()),
                ('company', models.ForeignKey(related_name='_employees_company', to='companies101rdb.Company')),
                ('department', models.ForeignKey(related_name='_employees_department', to='companies101rdb.Department')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='department',
            name='manager',
            field=models.OneToOneField(related_name='managed_departement', null=True, blank=True, to='companies101rdb.Employee'),
            preserve_default=True,
        ),
    ]
