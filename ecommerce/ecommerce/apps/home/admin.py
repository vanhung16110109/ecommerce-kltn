from django.contrib import admin
from .models import Province, District
# Register your models here.

class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['provinceid','name']

class DistrictAdmin(admin.ModelAdmin):
    list_display = ['districtid','name', 'provinceid']

admin.site.register(Province, ProvinceAdmin)
admin.site.register(District, DistrictAdmin)
# Register your models here.
