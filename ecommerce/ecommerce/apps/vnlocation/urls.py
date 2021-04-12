from django.urls import path, include
from apps.vnlocation.views import demo

urlpatterns = [
    path('', demo, name='demo'),
]