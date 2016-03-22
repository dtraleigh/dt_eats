from django.contrib import admin
from eats.models import District, Business, snapshot, tip

class district_admin(admin.ModelAdmin):
    fields = ('name', 'description', 'link', 'photo', 'district_map')
    list_display = ('name', 'link')

class business_admin(admin.ModelAdmin):
    list_display = ('name', 'date_added', 'district', 'not_local', 'open_date', 'close_date')

    actions = ['make_not_local', 'make_local']

    def make_not_local(self, request, queryset):
        queryset.update(not_local = True)

    def make_local(self, request, queryset):
        queryset.update(not_local = False)

    make_not_local.short_description = "Mark selected as not local"
    make_local.short_description = "Mark selected as local"

class snapshot_admin(admin.ModelAdmin):
    list_display = ('date', 'local_business_count', 'not_local_business_count')

class tip_admin(admin.ModelAdmin):
    list_display = ('name', 'district', 'description', 'date')

admin.site.register(District, district_admin)
admin.site.register(Business, business_admin)
admin.site.register(snapshot, snapshot_admin)
admin.site.register(tip, tip_admin)
