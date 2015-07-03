# coding=utf-8

from django.contrib import admin

from django.utils.html import format_html
#from django.core.urlresolvers import reverse
#from import_export.admin import ImportExportModelAdmin

from cyberhotel.models import \
    Residence, Salle, SalleDeBain, Chambre, \
    Resident, Locataire, Location, Reduction
from cyberhotel.models import ResidenceResource
from django.utils.translation import ugettext as _

from django.db.models.query import QuerySet

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


class SalleInline(admin.TabularInline):
    model = Salle
    #-- edit view
    classes = ('grp-collapse grp-open',)  # grappelli
    fields = ['numero', 'etage', 'enTravaux']
    extra = 0


class SalleDeBainInLine(admin.StackedInline):
    model = SalleDeBain
    #-- edit view
    classes = ('grp-collapse grp-closed',)
    fields = ['numero', 'etage', 'enTravaux', 'estSurLePallier', 'chambre']
    extra = 0


class ChambreInLine(admin.StackedInline):
    model = Chambre
    #-- edit view
    classes = ('grp-collapse grp-closed',)  # grappelli
    inline_classes = (
        'grp-collapse grp-closed',)  # grappelli # only for stackedInline
    fields = ['numero', 'etage', 'enTravaux', 'nbLitsSimples', 'nbLitsDoubles',
              'prix', 'estNonFumeur']
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

    def displayChambres(self, instance):
        return objectsToURL(instance.chambres(), sep=',')

    displayChambres.short_description = 'chambres'
    displayChambres.allow_tags = True

    def displayChambresUtiles(self, instance):
        return objectsToURL(instance.chambresUtiles(), sep='<br/>')

    displayChambresUtiles.short_description = 'chambresUtiles'
    displayChambresUtiles.allow_tags = True

    def displaySallesDeBain(self, instance):
        return objectsToURL(instance.sallesDeBain(), sep=',')

    displaySallesDeBain.short_description = 'sallesDeBain'
    displaySallesDeBain.allow_tags = True
    #-- edit view
    fieldsets = [
        ('',
         {'fields': [('nom', 'categorie'), ('etageMin', 'etageMax')],
          'classes': ['grp-collapse'],
          'description':
              'this is <a url="http://localhost:8000/admin/">some</a>'
              'text with <em>bold</em><br/>toto'}),
        # attribute and rols can be put in any order
        # see http://django-grappelli.readthedocs.org/en/latest/customization.html#rearrange-inlines
        (None,  #ignored
         {'fields': (),  # grappelli
          'classes': ("placeholder _salles-2-group",),
          'description': 'this is some text with <em>bold</em><br/>toto'}
         #ignored
        ),
        ('Additional information',
         {'fields': [('nbPlacesMax', 'tarifMoyen')],
          'classes': ['grp-collapse grp-closed']}),  #grappelli
    ]
    radio_fields = {
        # alternative to dropdown or raw_id for Choice/Dropdown
        "categorie": admin.HORIZONTAL}

    #-- list view
    actions_on_top = True
    actions_on_bottom = False  # no effect with grappelli
    inlines = [SalleInline, SalleDeBainInLine, ChambreInLine]
    list_display = ['nom', 'categorie', 'etageMin', 'etageMax', 'nbDeSalles',
                    'displayChambres', 'displaySallesDeBain',
                    'displayChambresUtiles']
    list_editable = ['categorie', 'etageMin', 'etageMax']

    list_filter = ['categorie', 'etageMin', 'etageMax']
    list_display_links = ['nom']
    # change_list_template = "admin/change_list_filter_sidebar.html"
    # grappelli
    search_fields = ['nom']

    list_select_related = True  # ?


# example of a view
class ResidencePrestige(Residence):
    class Meta(object):
        proxy = True


class ReadOnlySalleInline(ReadOnlyTabularInline, SalleInline):
    pass


class ResidencePrestigeAdmin(ReadOnlyAdmin, ResidenceAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(categorie='prestige')

    inlines = [ReadOnlySalleInline]
    # ,ROSalleDeBainInLine,ROChambreInLine]
    # readonly_fields = ['nom','etageMin','etageMax','categorie','salles']
    #-- list view
    # list_display = ['nom','categorie']
    # list_editable = []
    # inlines = []


#class EstResponsableDeInline(admin.TabularInline):
#  model = Resident.tuteurs.through
#  fk_name = 'from_resident'

class ResidentAdmin(admin.ModelAdmin):
    #-- list view
    list_display = ['nom', 'genre', 'age', 'estFumeur', 'conjoint',
                    'residence', 'chambreOccupee']
    list_editable = ['genre', 'age', 'estFumeur', 'conjoint', 'chambreOccupee']
    list_filter = ['age', 'genre', 'estFumeur', 'chambreOccupee']
    c = ['nom']
    #-- edit view
    fields = [("nom", "age", "genre"), ("chambreOccupee", "estFumeur"),
              'conjoint', 'tuteurs']
    # inlines = [ EstResponsableDeInline, ]


class SalleAdmin(admin.ModelAdmin):

    def displayResidence(self, instance): return objectToURL(
        instance.residence)

    displayResidence.short_description = 'residence'
    displayResidence.allow_tags = True

    readonly_fields = [displayResidence]
    #-- list view
    list_display = ['__unicode__', 'displayResidence', 'etage', 'enTravaux']
    list_display_links = ['__unicode__']
    #-- edit view


class SalleDeBainAdmin(admin.ModelAdmin):
    #-- list view
    list_display = ['__unicode__', 'residence', 'numero', 'etage', 'enTravaux',
                    'estSurLePallier', 'chambre']
    list_display_links = ['__unicode__']
    #-- edit view


# class DecadeBornListFilter(admin.SimpleListFilter):




# see https://docs.djangoproject.com/en/dev/ref/contrib/admin/#modeladmin-options
class EtageTypeListFilter(admin.SimpleListFilter):
    title = _('type d etage')
    parameter_name = 'etageType'

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        if qs.filter(etage__lte=1).exists():
            yield ('rdc', _('rdc'))
        if qs.filter(etage__gte=2).exists():
            yield ('autre', _('autre'))

    def queryset(self, request, queryset):
        if self.value() == 'rdc':
            return queryset.filter(etage__lte=1)
        if self.value() == 'autre':
            return queryset.filter(etage__gte=2)


class ChambreAdmin(admin.ModelAdmin):
    
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
    readonly_fields = ['nbDePlaces', 'occupants', 'occupantsList',
                       'displayResidence', 'displayOccupants']
    #-- list view
    list_display = ['__unicode__', 'displayResidence', 'etage', 'enTravaux',
                    'nbLitsSimples', 'nbLitsDoubles', 'prix', 'estNonFumeur',
                    'nbDeOccupants', 'nbDePlaces', 'displayOccupants']
    list_display_links = ['__unicode__']
    # change_list_template = "admin/change_list_filter_sidebar.html"  # grappelli
    list_filter = ['residence', 'residence__categorie', EtageTypeListFilter,
                   'etage', 'enTravaux', 'nbLitsSimples', 'nbLitsDoubles',
                   'estNonFumeur']
    search_fields = ['prix', 'residence__nom']
    ordering = ['residence', 'numero']
    list_per_page = 10
    #-- edit view
    fields = ['residence', ('numero', 'etage'), 'enTravaux',
              ('nbLitsSimples', 'nbLitsDoubles'), 'estNonFumeur', 'prix',
              'nbDePlaces', 'displayOccupants']


class LocataireAdmin(admin.ModelAdmin):
    pass


class ReductionInline(admin.TabularInline):
    model = Reduction
    extra = 0


class LocationAdmin(admin.ModelAdmin):
    list_display = ['locataire', 'chambreLouee', 'dateDepart', 'dateFin']
    inlines = [ReductionInline]


admin.site.register(Residence, ResidenceAdmin)
admin.site.register(Salle, SalleAdmin)
admin.site.register(SalleDeBain, SalleDeBainAdmin)
admin.site.register(Chambre, ChambreAdmin)
admin.site.register(Resident, ResidentAdmin)
admin.site.register(Locataire, LocataireAdmin)
admin.site.register(Location, LocationAdmin)
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
