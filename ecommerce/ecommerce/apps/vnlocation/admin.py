from django.contrib import admin
from .models import Province
# Register your models here.

class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['provinceid','name']


admin.site.register(Province, ProvinceAdmin)


# Register your models here.
