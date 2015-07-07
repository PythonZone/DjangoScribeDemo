# coding=utf-8


from __future__ import absolute_import, print_function

from .buildings import Category, Residence, Room, Bedroom, Bathroom
from .rents import Gender, Person, Resident, Tenant
from .rates import Rent, Discount, validateDomainPercentage

from .buildings import ResidenceResource




import django.db.models.options as options
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('computed_fields',)





