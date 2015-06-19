# coding=utf-8

from django.db import models

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=255)

    def employees_company(self):
        return self._salles.all()

    def departments(self):
        return self._departements.all()

    class Meta:
        computed_fields = ['employees_company', 'departments']

    # implicit fields: _salles, _departements

    def __unicode__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    salary = models.FloatField()
    company = models.ForeignKey(
        'Company',
        related_name='_employees_company')
    department = models.ForeignKey(
        'Department',
        related_name='_employees_department')
    # implicit fields: managed_departement

    def __unicode__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(
        'Company',
        related_name='_compartments'
    )
    manager = models.OneToOneField(  # ??? should it be on this side?
                                     'Employee',
                                     blank=True, null=True,
                                     related_name='managed_departement'
                                     # ??? what about its cardinality [0..1]
    )

    def employees_department(self):
        return self._employees_department.all()

    class Meta:
        computed_fields = ['employees_department', ]

    def __unicode__(self):
        return self.name
