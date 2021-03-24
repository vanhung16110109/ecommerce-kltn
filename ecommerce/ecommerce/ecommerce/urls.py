"""
Definition of urls for ecommerce.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView



urlpatterns = [

    path('admin/', admin.site.urls),
]
