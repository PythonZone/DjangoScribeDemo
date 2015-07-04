# coding=utf-8

from import_export import resources
import polymorphic
from django.db import models
from django.core.exceptions import ValidationError
#from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import ugettext as _

import django.db.models.options as options

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('computed_fields',)

CATEGORY = (
    ('economy', 'economy'),
    ('standard', 'standard'),
    ('premium', 'premium'),
    ('prestige', 'prestige'),
)


class Residence(models.Model):
    class Meta(object):
        computed_fields = [
            'bedrooms', 'nbOfBedrooms', 'usefulBedrooms',
            'bathrooms', 'rooms', 'nbOfRooms']

    name = models.CharField(max_length=60)
    floorMin = models.IntegerField(default=0)
    floorMax = models.IntegerField()
    category = models.CharField(max_length=10, choices=CATEGORY)
    maxNbOfFreeUnits = models.IntegerField(blank=True, null=True)  # TODO
    avgRate = models.FloatField(blank=True, null=True)  # TODO

    def bedrooms(self):
        return self.rooms().instance_of(Bedroom)

    # NotInUML
    def nbOfBedrooms(self):
        return len(self.bedrooms())

    def usefulBedrooms(self):
        return [s for s in self.bedrooms() if not s.isOutOfOrder]

    def bathrooms(self):
        return self.rooms().instance_of(Bathroom)

    # NotInUML
    def rooms(self):
        return self._rooms.all()

    # NotInUML
    def nbOfRooms(self):
        return len(self.rooms())

    def __unicode__(self):
        return self.name

    # for validating entity constraint
    def validateFloorOrder(self):
        if not (self.floorMin <= self.floorMax):
            raise ValidationError(
                _(u"the mininum floor is higher tha maximum floor"),
                code="floorOrder")

    def clean(self):
        self.validateFloorOrder()


class Room(polymorphic.PolymorphicModel):
    residence = models.ForeignKey(Residence, related_name="_rooms")
    floor = models.IntegerField()
    isOutOfOrder = models.BooleanField(default=False)
    number = models.IntegerField()

    def __unicode__(self):
        return str(self.number)

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
    isOnTheLanding = models.BooleanField(default=False)  # FIXME
    bedroom = models.ForeignKey(
        'Bedroom',
        related_name="_bedrooms",
        blank=True,
        null=True)

    def __unicode__(self):
        return str(self.number)


class Bedroom(Room):
    class Meta(object):
        computed_fields = [
            'nbOfUnits', 'occupants', 'nbDeOccupants', 'occupantsList']

    nbOfSingleBeds = models.IntegerField(
        default=1,
        verbose_name='number of single beds')
    nbOfDoubleBeds = models.IntegerField(default=0)
    rate = models.FloatField(blank=True, null=True)
    isNonSmoking = models.BooleanField(default=True)

    def nbOfUnits(self):
        return self.nbOfSingleBeds + self.nbOfDoubleBeds * 2

    def occupants(self):
        return list(self._occupants.all())

    # NotInUML
    def nbDeOccupants(self):
        return len(self.occupants())   # FIXME should use a query

    # NotInUML
    def occupantsList(self):
        return ",".join(str(o) for o in self.occupants())

    def __unicode__(self):
        return str(self.number)


GENDER = {
    ('male', 'male'),
    ('female', 'female'),
}


class Person(models.Model):
    class Meta(object):
        abstract = True

    name = models.CharField(max_length=40)
    age = models.IntegerField()
    gender = models.CharField(max_length=5, choices=GENDER)


class Resident(Person):
    isSmoker = models.NullBooleanField()
    occupiedRooms = models.ForeignKey(
        Bedroom,
        related_name="_occupants")
    consort = models.OneToOneField(
        "self",
        related_name="+",
        blank=True,
        null=True)
    tutors = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name='tutored',
        blank=True,
        null=True)

    def __unicode__(self):
        return self.name

    def residence(self):
        return self.occupiedRooms.residence

# NotInUML
class ResidenceResource(resources.ModelResource):
    class Meta(object):
        model = Residence


class Tenant(Resident):
    def paidRate(self):
        return 0  # TODO

    def __unicode__(self):
        return self.name


class Rent(models.Model):
    # TODO NotInUML (not directly) rentedBedroomS, singular(x)
    rentedBedroom = models.ForeignKey(
        Bedroom,
        # TODO NotInUML (not directly): rent  plural(x)
        related_name="_rents")
    tenant = models.ForeignKey(
        Tenant,
        related_name="_rents")
    # NotInUML
    startDate = models.DateField()
    # NotInUML
    dateFin = models.DateField()

    def discount(self):
        return 0  # TODO

    def rate(self):
        return 0  # TODO

    def __unicode__(self):
        return str(self.rentedBedroom.number) + "/" + self.tenant.name

# should be a top level function instead of a method of Discount
# because python 2 limitation for serialization in the context of django
# migration. See the following url for more information:
# https://docs.djangoproject.com/en/1.7/topics/migrations/#serializing-values
def validateDomainPercentage(percentage):
    if not (0 <= percentage and percentage <= 100):
        raise ValidationError(
            _(u"%s is not a percentage") % percentage,
            code="domainPercentage")

class Discount(models.Model):
    rent = models.ForeignKey(
        Rent,
        related_name="_discounts")

    percentage = models.IntegerField(validators=[validateDomainPercentage])
    #  percentage  = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
    label = models.CharField(max_length=10)


#  def user_link(self):
#    return '<a href="%s">%s</a>' % (reverse("admin:auth_user_change", args=(self.user.id,)) , escape(self.user))
#
#  user_link.allow_tags = True
#  user_link.short_description = "User" 
