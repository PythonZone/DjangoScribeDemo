# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import cyberhotel.models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('percentage', models.IntegerField(validators=[cyberhotel.models.validateDomainPercentage])),
                ('label', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('startDate', models.DateField()),
                ('dateFin', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Residence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('floorMin', models.IntegerField(default=0)),
                ('floorMax', models.IntegerField()),
                ('category', models.CharField(max_length=10, choices=[(b'economy', b'economy'), (b'standard', b'standard'), (b'premium', b'premium'), (b'prestige', b'prestige')])),
                ('maxNbOfFreeUnits', models.IntegerField(null=True, blank=True)),
                ('avgRate', models.FloatField(null=True, blank=True)),
            ],
            options={
                'computed_fields': ['bedrooms', 'nbOfBedrooms', 'usefulBedrooms', 'bathrooms', 'rooms', 'nbOfRooms'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Resident',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=5, choices=[(b'male', b'male'), (b'female', b'female')])),
                ('isSmoker', models.NullBooleanField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('floor', models.IntegerField()),
                ('isOutOfOrder', models.BooleanField(default=False)),
                ('number', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Bedroom',
            fields=[
                ('room_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cyberhotel.Room')),
                ('nbOfSingleBeds', models.IntegerField(default=1, verbose_name=b'number of single beds')),
                ('nbOfDoubleBeds', models.IntegerField(default=0)),
                ('rate', models.FloatField(null=True, blank=True)),
                ('isNonSmoking', models.BooleanField(default=True)),
            ],
            options={
                'computed_fields': ['nbOfUnits', 'occupants', 'nbDeOccupants', 'occupantsList'],
            },
            bases=('cyberhotel.room',),
        ),
        migrations.CreateModel(
            name='Bathroom',
            fields=[
                ('room_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cyberhotel.Room')),
                ('isOnTheLanding', models.BooleanField(default=False)),
                ('bedroom', models.ForeignKey(related_name='_bedrooms', blank=True, to='cyberhotel.Bedroom', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cyberhotel.room',),
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('resident_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cyberhotel.Resident')),
            ],
            options={
                'abstract': False,
            },
            bases=('cyberhotel.resident',),
        ),
        migrations.AddField(
            model_name='room',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_cyberhotel.room_set+', editable=False, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='room',
            name='residence',
            field=models.ForeignKey(related_name='_rooms', to='cyberhotel.Residence'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resident',
            name='consort',
            field=models.OneToOneField(related_name='+', null=True, blank=True, to='cyberhotel.Resident'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resident',
            name='occupiedRooms',
            field=models.ForeignKey(related_name='_occupants', to='cyberhotel.Bedroom'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resident',
            name='tutors',
            field=models.ManyToManyField(related_name='tutored', null=True, to='cyberhotel.Resident', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rent',
            name='rentedBedroom',
            field=models.ForeignKey(related_name='_rents', to='cyberhotel.Bedroom'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rent',
            name='tenant',
            field=models.ForeignKey(related_name='_rents', to='cyberhotel.Tenant'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='discount',
            name='rent',
            field=models.ForeignKey(related_name='_discounts', to='cyberhotel.Rent'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='ResidencePrestige',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('cyberhotel.residence',),
        ),
    ]
