from django.shortcuts import render


# Create your views here.
#checkout online
def checkout_online(request):
    return render(request, 'checkoutonline.html', {})


#checkout_offline
def checkout_offline(request):
    return render(request, 'checkoutoffline.html', {})


def checkout(request):
    #setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context={
        'category':category,
        'setting': setting
    }
    return render(request, './checkout.html', context)

