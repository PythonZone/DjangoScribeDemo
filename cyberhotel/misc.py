# coding=utf-8
from django.contrib import admin
from django.db.models.query import QuerySet
from django.utils.html import format_html



#------- helpers --------------------------------------------------------------


# COULD BE USEFUL TO HAVE A LOOK AT django-admin-easy
#  https://github.com/ebertti/django-admin-easy

def htmlTooltip(o):
    r = "<strong>%s %s</strong><br/>" % (o._meta.object_name, str(o))
    for field in o._meta.fields:
        name = field.name
        type_ = field.get_internal_type()
        card = "[0..1]" if field.null else ""
        if type_ in ["ForeignKey", "OneToOneField"]:
            type_ = type_ + "(" + field.related.parent_model.__name__ + ")"
        value = str(field._get_val_from_obj(o))
        value2 = str(o.__getattribute__(name))
        if value2 != value:
            value = value + ' => "' + value2 + '"'
        r += "%s : %s%s = %s<br/>" % (name, type_, card, value)
    if hasattr(o._meta, "computed_fields"):
        computed_fields = o._meta.computed_fields
        for opname in computed_fields:
            value = o.__getattribute__(opname)()
            if isinstance(value, (tuple, list, QuerySet)) and not isinstance(
                    value, basestring):
                value = ", ".join([str(x) for x in value])
            value = str(value)
            r += "<em>%s</em>() = %s <br/>" % (opname, value)
    return r

def objectToURL(o):
    table = o.__class__.__name__.lower()
    url = "/admin/cyberhotel/" + table + "/" + str(o.id)
    tooltip = htmlTooltip(o)
    # tooltip = "coucou"
    return format_html("<a href='" + url + "' class='tooltip'>" + str(
        o) + "<span>" + tooltip + "</span></a>")

def objectsToURL(coll, sep='<br/>'):
    return format_html(sep.join([objectToURL(o) for o in coll]))


class ReadOnlyAdmin(admin.ModelAdmin):
    readonly_fields = []
    list_editable = []

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
               [field.name for field in obj._meta.fields]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(ReadOnlyAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class ReadOnlyTabularInline(admin.TabularInline):
    extra = 0
    can_delete = False
    editable_fields = []
    readonly_fields = []
    exclude = []

    def get_readonly_fields(self, request, obj=None):
        return \
            list(self.readonly_fields) + \
            [field.name for field in self.model._meta.fields
             if field.name not in self.editable_fields and
             field.name not in self.exclude]

    def has_add_permission(self, request):
        return False

