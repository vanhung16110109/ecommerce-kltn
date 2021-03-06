from django.contrib import admin
from apps.account.models import UserProfile
# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'address', 'phone', 'city', 'image_tag']

admin.site.register(UserProfile, UserProfileAdmin)