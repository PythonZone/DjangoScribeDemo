# coding=utf-8

from django.contrib import admin
from demo_scrapy.models import Residence, VilleMere, TypeDeLogement


class ResidenceAdmin(admin.ModelAdmin):
    model = Residence
    list_display = ['name', 'url', 'villeMere', 'city']


class VilleMereAdmin(admin.ModelAdmin):
    model = VilleMere
    list_display = ['name', 'url']


class TypeDeLogementAdmin(admin.ModelAdmin):
    model = TypeDeLogement
    list_display = ['name']


admin.site.register(Residence, ResidenceAdmin)
admin.site.register(VilleMere, VilleMereAdmin)
admin.site.register(TypeDeLogement, TypeDeLogementAdmin)
