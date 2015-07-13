# coding=utf-8

from __future__ import absolute_import, print_function

from django.contrib import admin
#from django.core.urlresolvers import reverse
#from import_export.admin import ImportExportModelAdmin

from ..models import \
    Residence, Room, Bathroom, Bedroom, \
    Resident, Tenant, Rent, ResidencePrestige, Discount

from .buildings import \
    ResidenceAdmin, RoomAdmin, BathroomAdmin, BedroomAdmin, \
    ResidencePrestigeAdmin
from .rents import \
    ResidentAdmin, TenantAdmin
from .rates import \
    RentAdmin


admin.site.register(Residence, ResidenceAdmin)
admin.site.register(ResidencePrestige, ResidencePrestigeAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Bathroom, BathroomAdmin)
admin.site.register(Bedroom, BedroomAdmin)
admin.site.register(Resident, ResidentAdmin)
admin.site.register(Tenant, TenantAdmin)
admin.site.register(Rent, RentAdmin)


# ===== introspection of an django object ========================
# http://stackoverflow.com/questions/2233883/get-all-related-django-model-objects

# ======  add a user to the creator of an object ========
# # app/models.py

# from https://code.djangoproject.com/wiki/CookBookNewformsAdminAndUser

# from django.db import models
# from django.contrib.auth.models import User

# class Post(models.Model):
# user = models.ForeignKey(User)
# content = models.TextField()

# class Comment(models.Model):
# post = models.ForeignKey(Post)
# user = models.ForeignKey(User)
# content = models.TextField()

# # app/admin.py

# from app.models import Post, Comment
# from django.contrib import admin

# class CommentInline(admin.TabularInline):
# model = Comment
# fields = ('content',)

# class PostAdmin(admin.ModelAdmin):

# fields= ('content',)
# inlines = [CommentInline]

# def save_model(self, request, obj, form, change):
# obj.user = request.user
# obj.save()

# def save_formset(self, request, form, formset, change):
# if formset.model == Comment:
# instances = formset.save(commit=False)
# for instance in instances:
# instance.user = request.user
# instance.save()
# else:
# formset.save()

# admin.site.register(Post, PostAdmin)
