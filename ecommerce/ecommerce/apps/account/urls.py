from django.urls import path, include
from apps.account.views import account_login, account_register, account_logout, account_information_view, account_information_update, account_password_update


urlpatterns = [
    path('login/', account_login, name='account_login'),
    path('register/', account_register, name='account_register'),
    path('logout/', account_logout, name='account_logout'),
    path('information/', account_information_view, name='account_information_view'),
    path('information/', account_information_update, name='account_information_update'),
    path('changepassword/', account_password_update, name='account_password_update'), 
]