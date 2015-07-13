# coding=utf-8

from __future__ import absolute_import, print_function

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

import polymorphic
from import_export import resources


# Transform: Enumeration
# Design: https://docs.djangoproject.com/en/1.8/ref/models/fields/#django.db.models.Field.choices
# Could be improved with a text for default
# identifier in minMaj for PyAlaOCL
# Variant: coding as integers
# Variant: using https://github.com/bigjason/django-choices (only string)
class Category(object):
    economy = 'economy'
    standard = 'standard'
    premium = 'premium'
    prestige = 'prestige'
    CHOICES = (
        (economy, _('Economy')),
        (standard, _('Standard')),
        (premium, _('Premium')),
        (prestige, _('Prestige')),
    )
    MAX_LENGTH = 8


class Residence(models.Model):

    class Meta(object):
        computed_fields = [
            'bedrooms', 'nbOfBedrooms', 'usefulBedrooms',
            'bathrooms', 'rooms', 'nbOfRooms']

    #---- structure -----------------------------------------------------------

    floorMin = models.IntegerField(
        default=0,
        verbose_name="floor minimum",
    )

    floorMax = models.IntegerField(
        verbose_name="floor maximum",
    )

    category = models.CharField(
        choices=Category.CHOICES,
        max_length=Category.MAX_LENGTH,
        # TODO: add validator django-choices
        # validators=[Category.validator]
    )

    name = models.CharField(
        max_length=60,
    )

    # TODO
    # DerivedAttribute
    maxNbOfFreeUnits = models.IntegerField(
        blank=True,
        null=True,
    )

    # TODO
    # DerivedAttribute
    avgRate = models.FloatField(
        blank=True,
        null=True,
    )


    #---- title ---------------------------------------------------------------

    def __unicode__(self):
        return self.name


    #---- computed ------------------------------------------------------------

    # QueryOperation
    def bedrooms(self):
        return self.rooms().instance_of(Bedroom)

    # NotInUML
    def nbOfBedrooms(self):
        return len(self.bedrooms())

    # QueryOperation
    def usefulBedrooms(self):
        return [s for s in self.bedrooms() if not s.isOutOfOrder]

    # QueryOperation
    def bathrooms(self):
        return self.rooms().instance_of(Bathroom)

    # NotInUML
    def rooms(self):
        return self._rooms.all()

    # NotInUML
    def nbOfRooms(self):
        return len(self.rooms())


    #---- invariants ----------------------------------------------------------

    # LocalInvariant
    def floorOrder(self):
        return self.floorMin <= self.floorMax

    # for validating entity constraint
    def validateFloorOrder(self):
        if not (self.floorOrder):
            raise ValidationError(
                _(u"the mininum floor is higher tha maximum floor"),
                code="floorOrder")

    def clean(self):
        self.validateFloorOrder()

# example of a view
class ResidencePrestige(Residence):
    class Meta(object):
        proxy = True





class Room(polymorphic.PolymorphicModel):

    #---- structure -----------------------------------------------------------
    residence = models.ForeignKey(
        Residence,
        related_name="_rooms",
    )

    floor = models.IntegerField(
    )

    isOutOfOrder = models.BooleanField(
        default=False,
    )

    number = models.IntegerField(
    )

    #---- title ---------------------------------------------------------------
    def __unicode__(self):
        return str(self.number)


    #---- invariants ----------------------------------------------------------
    def floorBetweenMinAndMax(self):
        if ( not (self.residence.floorMin <= self.floor
                  and self.floor <= self.residence.floorMax)):
            raise ValidationError(
                _('the floor must be between %i and %i')
                % (self.residence.floorMin,
                   self.residence.floorMax),
                code="floorBetweenMinAndMax")

    def clean(self):
        self.floorBetweenMinAndMax()




class Bathroom(Room):

    #---- structure -----------------------------------------------------------
    isOnTheLanding = models.BooleanField(
        default=False,
    )  # FIXME

    bedroom = models.ForeignKey(
        'Bedroom',
        related_name="_bedrooms",
        blank=True,
        null=True,
    )

    #---- title ---------------------------------------------------------------
    def __unicode__(self):
        return str(self.number)



class Bedroom(Room):

    class Meta(object):
        computed_fields = [
            'nbOfUnits', 'occupants', 'nbDeOccupants', 'occupantsList']


    #---- structure -----------------------------------------------------------
    nbOfSingleBeds = models.IntegerField(
        default=1,
        verbose_name='number of single beds',
    )

    nbOfDoubleBeds = models.IntegerField(
        default=0,
        verbose_name='number of double beds',
    )

    rate = models.FloatField(
        blank=True,
        null=True,
    )

    isNonSmoking = models.BooleanField(
        default=True,
    )

    #---- title ---------------------------------------------------------------
    def __unicode__(self):
        return str(self.number)

    def nbOfUnits(self):
        return self.nbOfSingleBeds + self.nbOfDoubleBeds * 2

    def occupants(self):
        return list(self._occupants.all())

    # NotInUML
    def nbDeOccupants(self):
        return len(self.occupants())  # FIXME should use a query

    # NotInUML
    def occupantsList(self):
        return ",".join(str(o) for o in self.occupants())


# TODO
# NotInUML
class ResidenceResource(resources.ModelResource):
    class Meta(object):
        model = Residence
