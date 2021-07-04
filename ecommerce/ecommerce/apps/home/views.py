from django.shortcuts import render
from django.http import HttpResponse
# from .forms import SearchForm
# from .models import ContactForm, ContactMessage
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
    product_slider_mini = Banner.objects.all().order_by('id')[5:8] #lay 2 phan tu cuoi cung cua mang
    product_lasted = Product.objects.all().order_by('-id')[:4]
    product_picked = Product.objects.all().order_by('?')[:4]
    product_all = Product.objects.all()
    page = "home"
    current_user = request.user
    image_default = "user.png"
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.variant.price * rs.quantity
    quantity = 0
    for rs in shopcart:
        quantity += rs.quantity
    context={
        'page': page,
        'category': category,
        'product_slider': product_slider,
        'product_slider_mini': product_slider_mini,
        'product_lasted': product_lasted,
        'product_picked': product_picked,
		'product_all': product_all,
		'total': total,
        'quantity': quantity,
        'image_default': image_default,
    }
    return render(request, './index.html', context)
