import json
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from apps.vnlocation import querydb
import sqlite3
from apps.order.models import ShopCart, Order, OrderProduct
from django.contrib.auth.decorators import login_required
import requests
from django.template.loader import render_to_string


mytoken = "62045ed5-d43f-11eb-81f5-a267211ac77c"


def transportfeeAPI(request):
    #lay thong tin tinh thanh pho
    headers={'Content-Type':'application/json', 'Token': mytoken}
    r = requests.get('https://online-gateway.ghn.vn/shiip/public-api/master-data/province', headers=headers)
    dataAPI_province = r.json()
    context = {
        'dataAPI_province': dataAPI_province,
    }
    return render(request, 'vnlocation/transportfeeAPI.html', context)


def ajaxAPIlocationdistrict(request):
    print(request)
    data = {}
    if request.POST.get('action') == 'post':
        ProvinceName = int(request.POST.get('ProvinceName'))        # ten thanh pho tra ve
        print(ProvinceName)
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
                'rendered_table1': render_to_string('vnlocation/transportfeeAPI2.html', context=context)
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
