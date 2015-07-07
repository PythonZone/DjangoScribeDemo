# coding=utf-8

from __future__ import absolute_import, print_function

from django.contrib import admin
from django.utils.translation import ugettext as _
from django.db.models.query import QuerySet
from django.utils.html import format_html
#from django.core.urlresolvers import reverse
#from import_export.admin import ImportExportModelAdmin

from .models import \
    Residence, Room, Bathroom, Bedroom, \
    Resident, Tenant, Rent, Discount
from .models import ResidenceResource

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


#------- helpers --------------------------------------------------------------------


class RoomInline(admin.TabularInline):
    model = Room
    #-- edit view
    classes = ('grp-collapse grp-open',)  # grappelli
    fields = ['number', 'floor', 'isOutOfOrder']
    extra = 0


class BathroomInLine(admin.StackedInline):
    model = Bathroom
    #-- edit view
    classes = ('grp-collapse grp-closed',)
    fields = ['number', 'floor', 'isOutOfOrder', 'isOnTheLanding', 'bedroom']
    extra = 0


class BedroomInLine(admin.StackedInline):
    model = Bedroom
    #-- edit view
    classes = ('grp-collapse grp-closed',)  # grappelli
    inline_classes = (
        'grp-collapse grp-closed',)  # grappelli # only for stackedInline
    fields = ['number', 'floor', 'isOutOfOrder',
              'nbOfSingleBeds',  'nbOfDoubleBeds',
              'rate', 'isNonSmoking']
    extra = 0


class ResidenceAdmin(admin.ModelAdmin):  #ImportExportModelAdmin):
    # display load data, dump data thanks to smuggler and grappelli adapted template
    # http://django-grappelli.readthedocs.org/en/2.5.4/thirdparty.html
    # the button are not display correctly with django
    # change_list_template = 'smuggler/change_list.html'  # https://github.com/semente/django-smuggler/
    # change_list_template = 'admin/cyberhotel/residence/change_list_bis.html'  # just a test. see templates directory

    class Media(object):
        css = {"all": ("/static/cyberhotel/residence/style.css",)}

    class Meta(object):
        permissions = (
            ("viewonly_residence",
             "View only residence (require change_residence")
        )

    resource_class = ResidenceResource  # import_export (?)

    def displayBedrooms(self, instance):
        return objectsToURL(instance.chambres(), sep=',')

    displayBedrooms.short_description = 'bedrooms'
    displayBedrooms.allow_tags = True

    def displayUsefulBedrooms(self, instance):
        return objectsToURL(instance.usefulBedrooms(), sep='<br/>')

    displayUsefulBedrooms.short_description = 'useful bedrooms'
    displayUsefulBedrooms.allow_tags = True

    def displayBathrooms(self, instance):
        return objectsToURL(instance.bathrooms(), sep=',')

    displayBathrooms.short_description = 'bathrooms'
    displayBathrooms.allow_tags = True

    #-- edit view
    fieldsets = [
        ('',
         {'fields': [('name', 'category'), ('floorMin', 'floorMax')],
          'classes': ['grp-collapse'],
          'description':
              'this is <a url="http://localhost:8000/admin/">some</a>'
              'text with <em>bold</em><br/>toto'}),
        # attribute and roles can be put in any order
        # see http://django-grappelli.readthedocs.org/en/latest/customization.html#rearrange-inlines
        (None,  #ignored
         {'fields': (),  # grappelli
          'classes': ("placeholder _rooms-2-group",),
          'description': 'this is some text with <em>bold</em><br/>toto'}
         #ignored
        ),
        ('Additional information',
         {'fields': [('maxNbOfFreeUnits', 'avgRate')],
          'classes': ['grp-collapse grp-closed']}),  #grappelli
    ]
    radio_fields = {
        # alternative to drop down or raw_id for Choice/Drop down
        "category": admin.HORIZONTAL}

    #-- list view
    actions_on_top = True
    actions_on_bottom = False  # no effect with grappelli
    inlines = [RoomInline, BathroomInLine, BedroomInLine]
    list_display = ['name', 'category', 'floorMin', 'floorMax', 'nbOfRooms',
                    'displayBedrooms', 'displayBathrooms',
                    'displayUsefulBedrooms']
    list_editable = ['category', 'floorMin', 'floorMax']

    list_filter = ['category', 'floorMin', 'floorMax']
    list_display_links = ['name']
    # change_list_template = "admin/change_list_filter_sidebar.html"
    # grappelli
    search_fields = ['name']

    list_select_related = True  # ?


# example of a view
class ResidencePrestige(Residence):
    class Meta(object):
        proxy = True


class ReadOnlyRoomInline(ReadOnlyTabularInline, RoomInline):
    pass


class ResidencePrestigeAdmin(ReadOnlyAdmin, ResidenceAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(category='prestige')

    inlines = [ReadOnlyRoomInline]
    # ,ROSalleDeBainInLine,ROChambreInLine]
    # readonly_fields = ['name','floorMin','floorMax','category','rooms']
    #-- list view
    # list_display = ['name','category']
    # list_editable = []
    # inlines = []


#class IsTutoredByInline(admin.TabularInline):
#  model = Resident.tutors.through
#  fk_name = 'from_resident'

class ResidentAdmin(admin.ModelAdmin):
    #-- list view
    list_display = ['name', 'gender', 'age', 'isSmoker', 'consort',
                    'residence', 'occupiedRooms']
    list_editable = ['gender', 'age', 'isSmoker', 'consort', 'occupiedRooms']
    list_filter = ['age', 'gender', 'isSmoker', 'occupiedRooms']
    c = ['name']
    #-- edit view
    fields = [("name", "age", "gender"), ("occupiedRooms", "isSmoker"),
              'consort', 'tutors']
    # inlines = [ IsTutoredByInline, ]


class RoomAdmin(admin.ModelAdmin):

    def displayResidence(self, instance): return objectToURL(
        instance.residence)

    displayResidence.short_description = 'residence'
    displayResidence.allow_tags = True

    readonly_fields = [displayResidence]
    #-- list view
    list_display = ['__unicode__', 'displayResidence', 'floor', 'isOutOfOrder']
    list_display_links = ['__unicode__']
    #-- edit view


class BathroomAdmin(admin.ModelAdmin):
    #-- list view
    list_display = ['__unicode__', 'residence', 'number', 'floor', 'isOutOfOrder',
                    'isOnTheLanding', 'bedroom']
    list_display_links = ['__unicode__']
    #-- edit view


# class DecadeBornListFilter(admin.SimpleListFilter):




# see https://docs.djangoproject.com/en/dev/ref/contrib/admin/#modeladmin-options
class FloorTypeListFilter(admin.SimpleListFilter):
    title = _('type d floor')
    parameter_name = 'etageType'

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        if qs.filter(floor__lte=1).exists():
            yield ('basement', _('basement'))
        if qs.filter(floor__gte=2).exists():
            yield ('other', _('other'))

    def queryset(self, request, queryset):
        if self.value() == 'basement':
            return queryset.filter(floor__lte=1)
        if self.value() == 'autre':
            return queryset.filter(floor__gte=2)


class BedroomAdmin(admin.ModelAdmin):

    def displayResidence(self, instance): return objectToURL(
        instance.residence)

    displayResidence.short_description = 'residence'
    displayResidence.allow_tags = True
    displayResidence.admin_order_field = 'residence'

    def displayOccupants(self, instance): return objectsToURL(
        instance._occupants.all())

    displayOccupants.short_description = 'occupants'
    displayOccupants.allow_tags = True
    # always put operation and display operation into readonly_fields:
    # this makes it possible to put them in list_display (list view) and fields view
    readonly_fields = ['nbOfUnits', 'occupants', 'occupantsList',
                       'displayResidence', 'displayOccupants']
    #-- list view
    list_display = ['__unicode__', 'displayResidence', 'floor', 'isOutOfOrder',
                    'nbOfSingleBeds', 'nbOfDoubleBeds', 'rate', 'isNonSmoking',
                    'nbDeOccupants', 'nbOfUnits', 'displayOccupants']
    list_display_links = ['__unicode__']
    # change_list_template = "admin/change_list_filter_sidebar.html"  # grappelli
    list_filter = ['residence', 'residence__category', FloorTypeListFilter,
                   'floor', 'isOutOfOrder', 'nbOfSingleBeds', 'nbOfDoubleBeds',
                   'isNonSmoking']
    search_fields = ['rate', 'residence_name']
    ordering = ['residence', 'number']
    list_per_page = 10
    #-- edit view
    fields = ['residence', ('number', 'floor'), 'isOutOfOrder',
              ('nbOfSingleBeds', 'nbOfDoubleBeds'), 'isNonSmoking', 'rate',
              'nbOfUnits', 'displayOccupants']


class TenantAdmin(admin.ModelAdmin):
    pass


class DiscountInline(admin.TabularInline):
    model = Discount
    extra = 0


class RentAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'rentedBedroom', 'startDate', 'dateFin']
    inlines = [DiscountInline]


admin.site.register(Residence, ResidenceAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Bathroom, BathroomAdmin)
admin.site.register(Bedroom, BedroomAdmin)
admin.site.register(Resident, ResidentAdmin)
admin.site.register(Tenant, TenantAdmin)
admin.site.register(Rent, RentAdmin)
admin.site.register(ResidencePrestige, ResidencePrestigeAdmin)

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
