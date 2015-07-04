# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies101rdb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='company',
            field=models.ForeignKey(related_name='_departments', to='companies101rdb.Company'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='department',
            name='manager',
            field=models.OneToOneField(related_name='_managed_department', null=True, blank=True, to='companies101rdb.Employee'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='employee',
            name='company',
            field=models.ForeignKey(related_name='_employees', to='companies101rdb.Company'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='employee',
            name='department',
            field=models.ForeignKey(related_name='_employees', to='companies101rdb.Department'),
            preserve_default=True,
        ),
    ]
