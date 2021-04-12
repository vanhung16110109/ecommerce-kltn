from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from apps.vnlocation import querydb
import sqlite3


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