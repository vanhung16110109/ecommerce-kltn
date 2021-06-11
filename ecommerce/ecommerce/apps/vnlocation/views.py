from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from apps.vnlocation import querydb
import sqlite3
from apps.order.models import ShopCart, Order, OrderProduct
from django.contrib.auth.decorators import login_required


def demo(request):
    province_name = querydb.show_province()
    province = []
    for i in province_name:
        #print(i[0])
        province.append(i[0])
    context = {
        'province':  province,
        'province_name': province_name,
    }
    return render(request, 'vnlocation/demo.html', context)


@login_required(login_url='/login') # Check login
def user_order_product(request):
    #category = Category.objects.all()
    current_user = request.user
    order_product = OrderProduct.objects.filter(user_id=current_user.id).order_by('-id')
    context = {#'category': category,
               'order_product': order_product,
               }
    return render(request, 'vnlocation/user_order_products.html', context)


@login_required(login_url='/login') # Check login
def user_order_product_detail(request,id,oid):
    #category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=oid)
    orderitems = OrderProduct.objects.filter(id=id,user_id=current_user.id)
    context = {
        #'category': category,
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'vnlocation/user_order_detail.html', context)