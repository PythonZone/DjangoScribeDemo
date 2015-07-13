# coding=utf-8

from django.contrib import admin

from ..models import \
    Discount

class DiscountInline(admin.TabularInline):
    model = Discount
    extra = 0


class RentAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'rentedBedroom', 'startDate', 'dateFin']
    inlines = [DiscountInline]

