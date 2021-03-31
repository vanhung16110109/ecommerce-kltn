from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
# from django.contrib.auth import authenticate, get_user_model, login, logout, update_session_auth_hash
# from django.contrib import messages
# from django.contrib.auth.models import User 
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import PasswordChangeForm


# login
def account_login(request):
    return render(request, 'account/login.html', {})


#register
def account_register(request):
    return render(request, 'account/register.html', {})


#logout
def account_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


#change information
def account_information(request):
    return render(request, 'account/information.html')


#change password
def account_password(request):
    return render(request, 'account/changepassword.html')