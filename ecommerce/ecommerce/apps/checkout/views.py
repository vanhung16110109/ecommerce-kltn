from django.shortcuts import render


# Create your views here.
#checkout online
def checkout_online(request):
    return render(request, 'checkoutonline.html', {})


#checkout_offline
def checkout_offline(request):
    return render(request, 'checkoutoffline.html', {})
