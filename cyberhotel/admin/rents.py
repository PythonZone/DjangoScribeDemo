from django.contrib import admin

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

class TenantAdmin(admin.ModelAdmin):
    pass
