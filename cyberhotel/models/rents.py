# coding=utf-8

from __future__ import absolute_import, print_function

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from .buildings import Bedroom

class Gender(object):
    male = 'male'
    female = 'female'
    CHOICES = (
        (male, _('Male')),
        (female, _('Female')),
    )
    MAX_LENGTH = 8


class Person(models.Model):

    class Meta(object):
        abstract = True

    #---- structure -----------------------------------------------------------

    name = models.CharField(
        max_length=40,
    )

    age = models.IntegerField(
    )

    gender = models.CharField(
        max_length=5,
        choices=Gender.CHOICES,
    )


class Resident(Person):

    #---- structure -----------------------------------------------------------

    isSmoker = models.NullBooleanField(
    )

    occupiedRooms = models.ForeignKey(
        Bedroom,
        related_name="_occupants",
    )

    consort = models.OneToOneField(
        "self",
        related_name="+",
        blank=True,
        null=True,
    )

    tutors = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name='tutored',
        blank=True,
        null=True,
    )

    #---- title ---------------------------------------------------------------

    def __unicode__(self):
        return self.name

    #---- computed ------------------------------------------------------------

    def residence(self):
        return self.occupiedRooms.residence







class Tenant(Resident):
    def paidRate(self):
        return 0  # TODO

    def __unicode__(self):
        return self.name
