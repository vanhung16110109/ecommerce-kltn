from django.urls import path, include
from apps.vnlocation.views import transportfeeAPI


urlpatterns = [
    path('', transportfeeAPI, name='transportfeeAPI'),
]