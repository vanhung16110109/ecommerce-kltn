from django.urls import path
from apps.chatbot.views import chatbot


urlpatterns = [
    path('', chatbot, name='chatbot'),
]