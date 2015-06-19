# coding=utf-8

from django.contrib import admin

from .models import Food

class FoodAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_filter = (
        'tags',
    )


admin.site.register(Food, FoodAdmin)


