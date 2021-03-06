# coding=utf-8
# adapted from from https://github.com/gadventures/django-fsm-admin/blob/master/example/fsm_example/admin.py

from django.contrib import admin

from fsm_admin.mixins import FSMTransitionMixin
from .models import PublishableModel


# Example use of FSMTransitionMixin (order is important!)
class PublishableModelAdmin(FSMTransitionMixin, admin.ModelAdmin):
    list_display = (
        'name',
        'display_from',
        'display_until',
        'state',
    )
    list_filter = (
        'state',
    )
    readonly_fields = (
        'state',
    )


admin.site.register(PublishableModel, PublishableModelAdmin)
