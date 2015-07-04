# coding=utf-8

from django.db import models

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=255)

    def employees(self):
        return self._employees.all()

    def departments(self):
        return self._departements.all()

    class Meta(object):
        computed_fields = ['employees', 'departments']

    # implicit fields: _rooms, _departements

    def __unicode__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    salary = models.FloatField()
    company = models.ForeignKey(
        'Company',
        related_name='_employees')
    department = models.ForeignKey(
        'Department',
        related_name='_employees')
    # implicit fields: managed_departement

    def __unicode__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(
        'Company',
        related_name='_departments'
    )
    manager = models.OneToOneField(  # ??? should it be on this side?
                                     'Employee',
                                     blank=True, null=True,
                                     related_name='_managed_department'
                                     # ??? what about its cardinality [0..1]
    )

    def employees(self):
        return self._employees.all()

    class Meta(object):
        computed_fields = ['employees', ]

    def __unicode__(self):
        return self.name
