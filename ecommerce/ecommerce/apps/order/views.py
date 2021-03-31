from django.shortcuts import render


# Create your views here.
def order_add(request):

    return render(request, 'order_add.html', {})


def order_delete(request):
    return render(request, 'order_delete.html', {})


def order_detail(request):
    return render(request, 'order_detail.html', {})
