from django.contrib import admin

# from .models import Setting, ContactMessage

# class SettingAdmin(admin.ModelAdmin):
#     list_display = ['title', 'company', 'update_at', 'status']

# class ContactMessageAdmin(admin.ModelAdmin):
#     list_display = ['name', 'subject', 'update_at', 'status']
#     readonly_fields =('name', 'subject', 'email', 'message','ip')
#     list_filter = ['status']

# # Register your models here.
# admin.site.register(Setting, SettingAdmin)
# admin.site.register(ContactMessage, ContactMessageAdmin)

#ver2
# from django.contrib import admin
# from .models import Province, District
# # Register your models here.

# class ProvinceAdmin(admin.ModelAdmin):
#     list_display = ['provinceid','name']

# class DistrictAdmin(admin.ModelAdmin):
#     list_display = ['districtid','name', 'provinceid']

# admin.site.register(Province, ProvinceAdmin)
# admin.site.register(District, DistrictAdmin)


# # Register your models here.
