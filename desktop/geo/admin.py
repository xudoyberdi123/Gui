from django.contrib import admin

from .models import Region, District


class RegionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "ordering")


class Districtdmin(admin.ModelAdmin):
    list_display = ("id", "name", "region", "ordering")


admin.site.register(Region, RegionAdmin)
admin.site.register(District, Districtdmin)
