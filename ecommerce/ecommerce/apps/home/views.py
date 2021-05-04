from django.shortcuts import render
from django.http import HttpResponse
# from .forms import SearchForm
from .models import ContactForm, ContactMessage
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from apps.product.models import Category, Product, Banner
import json
from apps.account.models import UserProfile
from django.contrib.auth.decorators import login_required
from apps.order.models import ShopCart


# Create your views here.
# @login_required(login_url='/login')
def home_page(request):
    category = Category.objects.all()
    product_slider = Banner.objects.all().order_by('id')[:4]
    product_lasted = Product.objects.all().order_by('-id')[:4]
    product_picked = Product.objects.all().order_by('?')[:4]
    page = "home"
    current_user = request.user
    image_default = "user.png"
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity
    quantity = 0
    for rs in shopcart:
        quantity += rs.quantity
    context={
        'page': page,
        'category': category,
        'product_slider': product_slider,
        'product_lasted': product_lasted,
        'product_picked': product_picked,
		'total': total,
        'quantity': quantity,
        'image_default': image_default,
    }
    return render(request, './index.html', context)


# def about_us(request):
#     setting = Setting.objects.get(pk=1)
#     category = Category.objects.all()
#     context={
#         'category':category,
#         'setting': setting
#     }
#     return render(request, './about.html', context)


# def contact(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             data = ContactMessage()
#             data.name = form.cleaned_data['name']
#             data.email = form.cleaned_data['email']
#             data.subject = form.cleaned_data['subject']
#             data.message = form.cleaned_data['message']
#             data.ip = request.META.get('REMOTE_ADDR')
#             data.save()
#             messages.success(request, "Your message has be sent. Thanks you for your message.")
#             return HttpResponseRedirect('/contact')

#     setting = Setting.objects.get(pk=1)
#     category = Category.objects.all()
#     form = ContactForm
#     context={
#         'category':category,
#         'setting': setting,
#         'form': form
#     }
#     return render(request, './contact.html', context)



