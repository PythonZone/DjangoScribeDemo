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
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateDepart', models.DateField()),
                ('dateFin', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Reduction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('taux', models.IntegerField(validators=[cyberhotel.models.validate_reduction_taux])),
                ('label', models.CharField(max_length=10)),
                ('location', models.ForeignKey(related_name='_reductions', to='cyberhotel.Location')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Residence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=60)),
                ('etageMin', models.IntegerField(default=0)),
                ('etageMax', models.IntegerField()),
                ('categorie', models.CharField(max_length=10, choices=[(b'economique', b'economique'), (b'standard', b'standard'), (b'premium', b'premium'), (b'prestige', b'prestige')])),
                ('nbPlacesMax', models.IntegerField(null=True, blank=True)),
                ('tarifMoyen', models.FloatField(null=True, blank=True)),
            ],
            options={
                'computed_fields': ['chambres', 'nbDeChambres', 'chambresUtiles', 'sallesDeBain', 'salles', 'nbDeSalles'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Resident',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=40)),
                ('age', models.IntegerField()),
                ('genre', models.CharField(max_length=5, choices=[(b'femme', b'femme'), (b'homme', b'homme')])),
                ('estFumeur', models.NullBooleanField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Locataire',
            fields=[
                ('resident_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cyberhotel.Resident')),
            ],
            options={
                'abstract': False,
            },
            bases=('cyberhotel.resident',),
        ),
        migrations.CreateModel(
            name='Salle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('etage', models.IntegerField()),
                ('enTravaux', models.BooleanField(default=False)),
                ('numero', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Chambre',
            fields=[
                ('salle_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cyberhotel.Salle')),
                ('nbLitsSimples', models.IntegerField(default=1, verbose_name=b'nb de lits simples')),
                ('nbLitsDoubles', models.IntegerField(default=0)),
                ('prix', models.FloatField(null=True, blank=True)),
                ('estNonFumeur', models.BooleanField(default=True)),
            ],
            options={
                'computed_fields': ['nbDePlaces', 'occupants', 'nbDeOccupants', 'occupantsList'],
            },
            bases=('cyberhotel.salle',),
        ),
        migrations.CreateModel(
            name='SalleDeBain',
            fields=[
                ('salle_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cyberhotel.Salle')),
                ('estSurLePallier', models.BooleanField(default=False)),
                ('chambre', models.ForeignKey(related_name='_sallesDeBains', blank=True, to='cyberhotel.Chambre', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cyberhotel.salle',),
        ),
        migrations.AddField(
            model_name='salle',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_cyberhotel.salle_set+', editable=False, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='salle',
            name='residence',
            field=models.ForeignKey(related_name='_salles', to='cyberhotel.Residence'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resident',
            name='chambreOccupee',
            field=models.ForeignKey(related_name='_occupants', to='cyberhotel.Chambre'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resident',
            name='conjoint',
            field=models.OneToOneField(related_name='+', null=True, blank=True, to='cyberhotel.Resident'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resident',
            name='tuteurs',
            field=models.ManyToManyField(related_name='tutores', null=True, to='cyberhotel.Resident', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='chambreLouee',
            field=models.ForeignKey(related_name='_locations', to='cyberhotel.Chambre'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='locataire',
            field=models.ForeignKey(related_name='_locations', to='cyberhotel.Locataire'),
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
