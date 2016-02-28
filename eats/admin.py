from django.contrib import admin
from eats.models import District, Business, snapshot

class district_admin(admin.ModelAdmin):
    fields = ('name', 'description', 'link', 'photo', 'district_map')
    list_display = ('name', 'link')

class business_admin(admin.ModelAdmin):
    fields = ('name', 'district', 'link', 'description',
               'display_on_site', 'has_outdoor_seating', 'is_temp_closed',
              'is_eats', 'is_drinks', 'is_coffee', 'not_local',
              'latitude', 'longitude')
    list_display = ('name', 'district', 'not_local', 'display_on_site')

    actions = ['make_not_local', 'make_local']

    def make_not_local(self, request, queryset):
        queryset.update(not_local = True)

    def make_local(self, request, queryset):
        queryset.update(not_local = False)

    make_not_local.short_description = "Mark selected as not local"
    make_local.short_description = "Mark selected as local"

class snapshot_admin(admin.ModelAdmin):
    list_display = ('date', 'local_business_count', 'not_local_business_count')

admin.site.register(District, district_admin)
admin.site.register(Business, business_admin)
admin.site.register(snapshot, snapshot_admin)
