import json
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from apps.vnlocation import querydb
import sqlite3
from apps.order.models import ShopCart, Order, OrderProduct
from django.contrib.auth.decorators import login_required
import requests
from django.template.loader import render_to_string
from apps.home.models import StoreAddress
from apps.order.models import ShopCart


mytoken = "62045ed5-d43f-11eb-81f5-a267211ac77c"


def demo(request):
    return render(request,'vnlocation/ggapi.html',{})

def transportfeeAPI(request):
    #lay thong tin tinh thanh pho
    headers={'Content-Type':'application/json', 'Token': mytoken}
    r = requests.get('https://online-gateway.ghn.vn/shiip/public-api/master-data/province', headers=headers)
    dataAPI_province = r.json()
    storeaddress = StoreAddress.objects.filter(id=1)
    print(storeaddress)
    context = {
        'dataAPI_province': dataAPI_province,
        'storeaddress': storeaddress
    }
    return render(request, 'vnlocation/transportfeeAPI.html', context)


def ajaxAPIlocationdistrict(request):
    #print(request)
    data = {}
    if request.POST.get('action') == 'post':
        ProvinceName = int(request.POST.get('ProvinceName'))        # ten thanh pho tra ve
        #print(ProvinceName)
        #lay thong tin tinh thanh pho
        headers={'Content-Type':'application/json', 'Token': mytoken}
        r = requests.get('https://online-gateway.ghn.vn/shiip/public-api/master-data/province', headers=headers)
        dataAPI_province = r.json()
        #lay thong tin quan huyen
        json_district = {"province_id": ProvinceName}
        r = requests.get('https://online-gateway.ghn.vn/shiip/public-api/master-data/district', headers=headers, json=json_district)
        dataAPI_district = r.json()
        context = {
            'dataAPI_province': dataAPI_province,
            'ProvinceName': ProvinceName,
            'dataAPI_district': dataAPI_district
        }
        data = {'rendered_table': render_to_string('vnlocation/transportfeeAPI1.html', context=context),
                'rendered_table1': render_to_string('vnlocation/transportfeeAPI2.html', context=context),
        }
        return JsonResponse(data)
        
    return JsonResponse(data)


def ajaxAPIlocationward(request):
    data = {}
    if request.POST.get('action') == 'post':
        headers={'Content-Type':'application/json', 'Token': mytoken}
        DistrictName = int(request.POST.get('DistrictName'))
        json_ward = {"district_id": DistrictName}
        r = requests.get('https://online-gateway.ghn.vn/shiip/public-api/master-data/ward', headers=headers, json=json_ward)
        dataAPI_ward = r.json()
        context = {
            'dataAPI_ward': dataAPI_ward
        }
        data = {'rendered_table': render_to_string('vnlocation/transportfeeAPI2.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)


def ajaxGHTK(request):
    data = {}
    storeaddress = StoreAddress.objects.filter(id=1)
    print(storeaddress)
    for i in storeaddress:
        adress_id = int(i.city)
    #print(adress_id)
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.variant.price * rs.quantity
    total_order = total
    #transport_fee = 0  # phí vận chuyển
    if request.POST.get('action') == 'post':
        ghtk = request.POST.get('ghtk')
        print(ghtk)
        ProvinceName = int(request.POST.get('ProvinceName'))
        #print(ProvinceName)
        if adress_id == ProvinceName:
            transport_fee = 30
            total = (total*1000 + 30)/1000
        else:
            transport_fee = 40
            total = (total*1000 + 40)/1000
        context = {
            'ghtk': ghtk,
            'total_order': total_order,			# tổng tiền order
            'transport_fee': transport_fee,
            'total': total  # tổng tiền thanh toán
        }
        data = {'rendered_table': render_to_string('checkout/total.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)


def ajaxGHN(request):
    data = {}
    storeaddress = StoreAddress.objects.filter(id=1)
    print(storeaddress)
    for i in storeaddress:
        adress_id = int(i.city)
    print(adress_id)
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.variant.price * rs.quantity
    total_order = total
    #transport_fee = 0  # phí vận chuyển
    if request.POST.get('action') == 'post':
        ghtk = request.POST.get('ghn')
        print(ghtk)
        ProvinceName = int(request.POST.get('ProvinceName'))
        print(ProvinceName)
        if adress_id == ProvinceName:
            transport_fee = 37
            total = (total*1000 + 37)/1000
        else:
            transport_fee = 47
            total = (total*1000 + 47)/1000
        context = {
            'ghtk': ghtk,
            'total_order': total_order,			# tổng tiền order
            'transport_fee': transport_fee,
            'total': total  # tổng tiền thanh toán
        }
        data = {'rendered_table': render_to_string('checkout/total.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)


def ajaxGHTK_online(request):
    data = {}
    storeaddress = StoreAddress.objects.filter(id=1)
    print(storeaddress)
    for i in storeaddress:
        adress_id = int(i.city)
    #print(adress_id)
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.variant.price * rs.quantity
    total_order = total
    #transport_fee = 0  # phí vận chuyển
    if request.POST.get('action') == 'post':
        ghtk = request.POST.get('ghtk')
        print(ghtk)
        ProvinceName = int(request.POST.get('ProvinceName'))
        #print(ProvinceName)
        if adress_id == ProvinceName:
            transport_fee = 30000
            total_new = int((total*1000 + 30)*1000)
        else:
            transport_fee = 40000
            total_new = int((total*1000 + 40)*1000)
        print(total_new)
        context = {
            'ghtk': ghtk,
            'total_order': total_order,			# tổng tiền order
            'transport_fee': transport_fee,
            'total_new': total_new  # tổng tiền thanh toán
        }
        data = {'rendered_table': render_to_string('checkout/total-online.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)


def ajaxGHN_online(request):
    data = {}
    storeaddress = StoreAddress.objects.filter(id=1)
    print(storeaddress)
    for i in storeaddress:
        adress_id = int(i.city)
    print(adress_id)
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.variant.price * rs.quantity
    total_order = total
    #transport_fee = 0  # phí vận chuyển
    if request.POST.get('action') == 'post':
        ghtk = request.POST.get('ghn')
        print(ghtk)
        ProvinceName = int(request.POST.get('ProvinceName'))
        print(ProvinceName)
        if adress_id == ProvinceName:
            transport_fee = 37000
            total_new = int((total*1000 + 37)*1000)
        else:
            transport_fee = 47000
            total_new = int((total*1000 + 47)*1000)
        print(total_new)
        context = {
            'ghtk': ghtk,
            'total_order': total_order,			# tổng tiền order
            'transport_fee': transport_fee,
            'total_new': total_new  # tổng tiền thanh toán
        }
        data = {'rendered_table': render_to_string('checkout/total-online.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)
