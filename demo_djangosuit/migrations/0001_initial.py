# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('slug', models.CharField(max_length=64)),
                ('is_active', models.BooleanField()),
                ('order', models.IntegerField()),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name=b'children', blank=True, to='demo_djangosuit.Category', null=True)),
            ],
            options={
                'verbose_name_plural': 'Categories (django-mptt)',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('capital', models.BooleanField()),
                ('area', models.BigIntegerField(null=True, blank=True)),
                ('population', models.BigIntegerField(null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Cities (django-select2)',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Continent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('order', models.PositiveIntegerField()),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('code', models.CharField(help_text=b'ISO 3166-1 alpha-2 - two character country code', max_length=2)),
                ('independence_day', models.DateField(null=True, blank=True)),
                ('area', models.BigIntegerField(null=True, blank=True)),
                ('population', models.BigIntegerField(null=True, blank=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('description', models.TextField(help_text=b'Try and enter few some more lines', blank=True)),
                ('architecture', models.TextField(blank=True)),
                ('continent', models.ForeignKey(to='demo_djangosuit.Continent', null=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'Countries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fridge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('type', models.SmallIntegerField(choices=[(1, b'Tall'), (2, b'Normal'), (3, b'Short')])),
                ('description', models.TextField(blank=True)),
                ('is_quiet', models.BooleanField()),
                ('order', models.PositiveIntegerField()),
            ],
            options={
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImportExportItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('quality', models.SmallIntegerField(default=1, choices=[(1, b'Awesome'), (2, b'Good'), (3, b'Normal'), (4, b'Bad')])),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='KitchenSink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('help_text', models.CharField(help_text=b'Enter fully qualified name', max_length=64)),
                ('multiple_in_row', models.CharField(help_text=b'Help text for multiple', max_length=64)),
                ('multiple2', models.CharField(max_length=10, blank=True)),
                ('textfield', models.TextField(help_text=b'Try and enter few some more lines', verbose_name=b'Autosized textarea', blank=True)),
                ('file', models.FileField(upload_to=b'.', blank=True)),
                ('readonly_field', models.CharField(default=b'Some value here', max_length=127)),
                ('date', models.DateField(null=True, blank=True)),
                ('date_and_time', models.DateTimeField(null=True, blank=True)),
                ('date_widget', models.DateField(null=True, blank=True)),
                ('datetime_widget', models.DateTimeField(null=True, blank=True)),
                ('boolean', models.BooleanField(default=True)),
                ('boolean_with_help', models.BooleanField(help_text=b'Boolean field with help text')),
                ('horizontal_choices', models.SmallIntegerField(default=1, help_text=b'Horizontal choices look like this', choices=[(1, b'Awesome'), (2, b'Good'), (3, b'Normal'), (4, b'Bad')])),
                ('vertical_choices', models.SmallIntegerField(default=2, help_text=b'Some help on vertical choices', choices=[(1, b'Hot'), (2, b'Normal'), (3, b'Cold')])),
                ('choices', models.SmallIntegerField(default=3, help_text=b'Help text', choices=[(1, b'Tall'), (2, b'Normal'), (3, b'Short')])),
                ('hidden_checkbox', models.BooleanField()),
                ('hidden_choice', models.SmallIntegerField(default=2, blank=True, choices=[(1, b'Tall'), (2, b'Normal'), (3, b'Short')])),
                ('hidden_charfield', models.CharField(max_length=64, blank=True)),
                ('hidden_charfield2', models.CharField(max_length=64, blank=True)),
                ('enclosed1', models.CharField(max_length=64, blank=True)),
                ('enclosed2', models.CharField(max_length=64, blank=True)),
                ('country', models.ForeignKey(related_name=b'foreign_key_country', to='demo_djangosuit.Country')),
                ('linked_foreign_key', models.ForeignKey(related_name=b'foreign_key_linked', to='demo_djangosuit.Country')),
                ('raw_id_field', models.ForeignKey(blank=True, to='demo_djangosuit.Country', help_text=b'Regular raw ID field', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Microwave',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('type', models.SmallIntegerField(default=2, help_text=b'Choose wisely', choices=[(1, b'Tall'), (2, b'Normal'), (3, b'Short')])),
                ('is_compact', models.BooleanField()),
                ('order', models.PositiveIntegerField()),
                ('kitchensink', models.ForeignKey(to='demo_djangosuit.KitchenSink')),
            ],
            options={
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReversionedItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('quality', models.SmallIntegerField(default=1, choices=[(1, b'Awesome'), (2, b'Good'), (3, b'Normal'), (4, b'Bad')])),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WysiwygEditor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('redactor', models.TextField(verbose_name=b'Redactor small', blank=True)),
                ('redactor2', models.TextField(verbose_name=b'Redactor2', blank=True)),
                ('ckeditor', models.TextField(verbose_name=b'CKEditor', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='fridge',
            name='kitchensink',
            field=models.ForeignKey(to='demo_djangosuit.KitchenSink'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(to='demo_djangosuit.Country'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='city',
            unique_together=set([('name', 'country')]),
        ),
    ]
