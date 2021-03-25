from django.urls import path, include
from apps.account.views import account_login, account_register, account_logout, account_information, account_password


urlpatterns = [
    path('login/', account_login, name='account_login'),
    path('register/', account_register, name='account_register'),
    path('logout/', account_logout, name='account_logout'),
    path('information/', account_information, name='account_information'),
    path('changepassword/', account_password, name='account_password'), 
]