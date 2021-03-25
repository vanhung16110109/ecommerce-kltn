from django.urls import path
from apps.checkout.views import checkout_online, checkout_offline

urlpatterns = [
    path('checkout-online/', checkout_online, name='checkout_online'),
    path('checkout-offline/', checkout_offline, name='checkout_offline'),
]