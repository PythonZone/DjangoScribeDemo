# coding=utf-8
from __future__ import absolute_import, print_function

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from .buildings import Bedroom
from .rents import Tenant


class Rent(models.Model):

    #---- structure -----------------------------------------------------------

    # TODO NotInUML (not directly) rentedBedroomS, singular(x)
    rentedBedroom = models.ForeignKey(
        Bedroom,
        # TODO NotInUML (not directly): rent  plural(x)
        related_name="_rents",
    )

    tenant = models.ForeignKey(
        Tenant,
        related_name="_rents",
    )

    # NotInUML
    startDate = models.DateField(

    )

    # NotInUML
    dateFin = models.DateField(

    )

    #---- title ---------------------------------------------------------------
    def __unicode__(self):
        return str(self.rentedBedroom.number) + "/" + self.tenant.name

    #---- computed ------------------------------------------------------------

    def discount(self):
        return 0  # TODO

    def rate(self):
        return 0  # TODO





def discountDomainPercentage(percentage):
    return 0 <= percentage and percentage <= 100

# should be a top level function instead of a method of Discount
# because python 2 limitation for serialization in the context of django
# migration. See the following url for more information:
# https://docs.djangoproject.com/en/1.7/topics/migrations/#serializing-values

def validateDomainPercentage(percentage):
    if not discountDomainPercentage(percentage):
        raise ValidationError(
            '%s %s' % (_('is not a percentage'), percentage),
            code="domainPercentage",
        )

class Discount(models.Model):

    #---- structure -----------------------------------------------------------
    rent = models.ForeignKey(
        Rent,
        related_name="_discounts")

    percentage = models.IntegerField(
        validators=[validateDomainPercentage],

    )
    # Alternative:
    #    percentage = models.IntegerField(
    #         validators=[ MinValueValidator(0), MaxValueValidator(100) ]
    #    )

    label = models.CharField(max_length=10)


#  def user_link(self):
#    return '<a href="%s">%s</a>' % (reverse("admin:auth_user_change", args=(self.user.id,)) , escape(self.user))
#
#  user_link.allow_tags = True
#  user_link.short_description = "User"
