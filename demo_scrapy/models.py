# coding=utf-8

from django.db import models


class Residence(models.Model):
    name = models.CharField(max_length=80)
    url = models.URLField(max_length=80)
    description = models.TextField(
        null=True)  # important for fields that can cause problems
    city = models.CharField(max_length=80)
    images = models.TextField()
    villeMere = models.ForeignKey("VilleMere", blank=True, null=True,
                                  related_name="_residences")
    typesDeLogement = models.ManyToManyField("TypeDeLogement",
                                             related_name="_residences")

    def __unicode__(self):
        return self.name


class VilleMere(models.Model):
    name = models.CharField(max_length=80)
    url = models.URLField(max_length=80)
    # _residences inverse of Residence.villeMere
    def __unicode__(self):
        return self.name


class TypeDeLogement(models.Model):
    name = models.CharField(max_length=80)

    def __unicode__(self):
        return self.name

