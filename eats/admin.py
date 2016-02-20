from django.contrib import admin
from eats.models import District, Business

# admin.site.register(District)
class DistrictAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'link', 'photo', 'district_map']
    list_display = ('name', 'link')

# admin.site.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    fields = ['name', 'district', 'link', 'description',
               'display_on_site', 'has_outdoor_seating', 'is_temp_closed',
              'is_eats', 'is_drinks', 'is_coffee', 'not_local',
              'latitude', 'longitude']
    list_display = ('name', 'district', 'not_local', 'display_on_site')

    actions = ['make_not_local', 'make_local']

    def make_not_local(self, request, queryset):
        queryset.update(not_local = True)

    def make_local(self, request, queryset):
        queryset.update(not_local = False)

    make_not_local.short_description = "Mark selected as not local"
    make_local.short_description = "Mark selected as local"

admin.site.register(District, DistrictAdmin)
admin.site.register(Business, BusinessAdmin)
