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
from babel.numbers import format_number


mytoken = "62045ed5-d43f-11eb-81f5-a267211ac77c"		#giao hàng nhanh
mytoken_ghtk = "D85E94443Fe9647029c79A1E45d1837e35C7Cfec"


def demo(request):
	return render(request,'vnlocation/ggapi.html',{})


def transportfeeAPI(request):
	#lay thong tin tinh thanh pho
	headers={'Content-Type':'application/json', 'Token': mytoken}
	r = requests.get('https://online-gateway.ghn.vn/shiip/public-api/master-data/province', headers=headers)
	dataAPI_province = r.json()
	storeaddress = StoreAddress.objects.filter(id=1)
	#print(storeaddress)
	#lay thong tin quan huyen
	r = requests.get('https://online-gateway.ghn.vn/shiip/public-api/master-data/district', headers=headers)
	dataAPI_district = r.json()
	context = {
		'dataAPI_province': dataAPI_province,
		'storeaddress': storeaddress,
		'dataAPI_district':dataAPI_district
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
	for i in storeaddress:
		adress_id = int(i.city)			#không cần dùng
		shop_id = i.ShopID_GHN
		city_id = int(i.city)
		district_id = int(i.district)
		length = i.length
		width = i.width
		height = i.height
		weight = i.weight
	
	current_user = request.user
	shopcart = ShopCart.objects.filter(user_id=current_user.id)
	# gia tri order producted
	total = 0
	for rs in shopcart:
		total += rs.variant.price * rs.quantity
	#print(int(total*1000000))
	
	#so luong order producted
	quantity = 0
	for rs in shopcart:
		quantity += rs.quantity
	
	# Xử lí API GHN
	
	# tính hình thức vận chuyển
	# tỉnh thành, địa chỉ nhận hàng
	ProvinceName = int(request.POST.get('ProvinceName'))        #get id
	DistrictName = int(request.POST.get('DistrictName'))
	WardName = request.POST.get('WardName')
	headers={'Content-Type':'application/json', 'Token': mytoken}
	r = requests.get('https://online-gateway.ghn.vn/shiip/public-api/master-data/province', headers=headers)
	dataAPI_province = r.json()
	json_district = {"province_id": ProvinceName}
	r = requests.get('https://online-gateway.ghn.vn/shiip/public-api/master-data/district', headers=headers, json=json_district)
	dataAPI_district = r.json()
	json_ward = {"district_id": DistrictName}
	r = requests.get('https://online-gateway.ghn.vn/shiip/public-api/master-data/ward', headers=headers, json=json_ward)
	dataAPI_ward = r.json()
	for i in range(len(dataAPI_province['data'])):
			#print(dataAPI_province['data'][i].get("ProvinceID"))
		if (dataAPI_province['data'][i].get("ProvinceID"))==ProvinceName:
			province = dataAPI_province['data'][i].get("ProvinceName")
	for i in range(len(dataAPI_district['data'])):
		#print(dataAPI_province['data'][i].get("ProvinceID"))
		if (dataAPI_district['data'][i].get("DistrictID"))==DistrictName:
			district = dataAPI_district['data'][i].get("DistrictName")
	for i in range(len(dataAPI_ward['data'])):
		#print(dataAPI_ward['data'][i].get("WardCode"))
		if dataAPI_ward['data'][i].get("WardCode")==WardName:
			ward = dataAPI_ward['data'][i].get("WardName") 
	# địa chỉ gửi hàng
	for i in range(len(dataAPI_province['data'])):
		if (dataAPI_province['data'][i].get("ProvinceID"))==city_id:
			pick_province = dataAPI_province['data'][i].get("ProvinceName")
	json_district_shop = {"province_id": city_id}
	r = requests.get('https://online-gateway.ghn.vn/shiip/public-api/master-data/district', headers=headers, json=json_district_shop)
	json_district_shop = r.json()

	for i in range(len(json_district_shop['data'])):
		if json_district_shop['data'][i].get("DistrictID") == district_id:
			pick_district = json_district_shop['data'][i].get("DistrictName")
	print(pick_province)
	print(pick_district)
	
	# tính giá trị đơn hàng
	#print(int(total*1000000))
	#temp = int(total*1000000)
	# if temp < 20000000:
	# 	insurance_fee = temp
	# else:
	# 	insurance_fee = 20000000
	# print(insurance_fee)
	# tính giá cước
	insurance_fee = 3000000
	weight = weight*quantity
	headers={'Content-Type':'application/json', 'Token': mytoken_ghtk}
	json = {
		"pick_province": pick_province,
		"pick_district": pick_district,
		"province": province,
		"district": district,
		"ward": ward,
		"weight": weight,
		"value": insurance_fee,
		"transport": "fly",
		"tags": [1]
	}
	# "tags": [1] Gắn nhãn dễ vỡ cho đơn hàng. Truyền giá trị 1 vào mảng tags nếu là đơn dễ vỡ
	r = requests.get('https://services.giaohangtietkiem.vn/services/shipment/fee?', headers=headers, json=json)
	dataAPI_transport_fee = r.json()
		
	transport_fee = 0
	transport_fee = dataAPI_transport_fee['fee']['fee']
	total_order = int(float(total)*1000000)
	# phí vận chuyển
	if request.POST.get('action') == 'post':
		ghtk = request.POST.get('ghtk')
		#print(ghtk)
		total = total_order + transport_fee
		total_order = format_number(total_order, locale='de_DE')
		transport_fee = format_number(transport_fee, locale='de_DE')
		total = format_number(total, locale='de_DE')
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
	for i in storeaddress:
		adress_id = int(i.city)			#không cần dùng
		shop_id = i.ShopID_GHN
		district_id = int(i.district)
		length = i.length
		width = i.width
		height = i.height
		weight = i.weight
		
	current_user = request.user
	shopcart = ShopCart.objects.filter(user_id=current_user.id)
	# gia tri order producted
	total = 0
	for rs in shopcart:
		total += rs.variant.price * rs.quantity
	#print(int(total*1000000))
	
	#so luong order producted
	quantity = 0
	for rs in shopcart:
		quantity += rs.quantity
	# Xử lí API GHN
	
	# tính hình thức vận chuyển
	to_district = int(request.POST.get('DistrictName'))
	print(district_id)
	print(to_district)
	headers={'Content-Type':'application/json', 'Token': mytoken}
	json_district = {
		"shop_id": shop_id,
		"from_district": district_id,
		"to_district": to_district
	}
	r = requests.get('https://online-gateway.ghn.vn/shiip/public-api/v2/shipping-order/available-services', headers=headers, json=json_district)
	dataAPI_thongtin = r.json()
	ServiceID_API = []
	for i in dataAPI_thongtin['data']:
		ServiceID_API.append(i['service_type_id'])

	for i in range(len(ServiceID_API)):
		#print(ServiceID_API[i], type(ServiceID_API[i]))
		if ServiceID_API[i]==2:
			service_type_id = 2
		else:
			service_type_id = 1

	to_ward_code = request.POST.get('WardName')
	# tính giá trị đơn hàng
	#print(int(total*1000000))
	temp = int(total*1000000)
	if temp < 10000000:
		insurance_fee = temp
	else:
		insurance_fee = 10000000
	#print(insurance_fee)
	#print(to_ward_code, type(to_ward_code))
	# tính giá cước
	weight = weight*quantity
	json_district = {
		"from_district_id": district_id,			# gửi từ
		'service_type_id': service_type_id,			# hình thức vận chuyển
		"to_district_id": to_district,				# quận huyện
		"to_ward_code": to_ward_code,				# đến xã, phường
		"height": height,							# chiều cao đơn hàng								
		"length":length,							# Chiều dài đơn hàng
		"weight": weight,							# khối lượng của đơn hàng
		"width":width,								# chiều rộng của đơn hàng
		"insurance_fee": insurance_fee,				# giá trị đơn hàng
		}
	r = requests.get('https://online-gateway.ghn.vn/shiip/public-api/v2/shipping-order/fee', headers=headers, json=json_district)
	dataAPI_transport_fee = r.json()
	
	transport_fee = 0
	transport_fee = int(dataAPI_transport_fee['data']['total'])
	total_order = int(float(total)*1000000)
	# tempabc = float(total_order)
	# tempabc = tempabc/1000000
	# print(tempabc)
	#transport_fee = 0  # phí vận chuyển
	if request.POST.get('action') == 'post':
		ghtk = request.POST.get('ghn')
		#print(ghtk)
		total = total_order + transport_fee
		total_order = format_number(total_order, locale='de_DE')
		transport_fee = format_number(transport_fee, locale='de_DE')
		total = format_number(total, locale='de_DE')
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
	for i in storeaddress:
		adress_id = int(i.city)			#không cần dùng
		shop_id = i.ShopID_GHN
		city_id = int(i.city)
		district_id = int(i.district)
		length = i.length
		width = i.width
		height = i.height
		weight = i.weight
	
	current_user = request.user
	shopcart = ShopCart.objects.filter(user_id=current_user.id)
	# gia tri order producted
	total = 0
	for rs in shopcart:
		total += rs.variant.price * rs.quantity
	#print(int(total*1000000))
	
	#so luong order producted
	quantity = 0
	for rs in shopcart:
		quantity += rs.quantity
	
	# Xử lí API GHN
	
	# tính hình thức vận chuyển
	# tỉnh thành, địa chỉ nhận hàng
	ProvinceName = int(request.POST.get('ProvinceName'))        #get id
	DistrictName = int(request.POST.get('DistrictName'))
	WardName = request.POST.get('WardName')	
	headers={'Content-Type':'application/json', 'Token': mytoken}
	r = requests.get('https://online-gateway.ghn.vn/shiip/public-api/master-data/province', headers=headers)
	dataAPI_province = r.json()
	json_district = {"province_id": ProvinceName}
	r = requests.get('https://online-gateway.ghn.vn/shiip/public-api/master-data/district', headers=headers, json=json_district)
	dataAPI_district = r.json()
	json_ward = {"district_id": DistrictName}
	r = requests.get('https://online-gateway.ghn.vn/shiip/public-api/master-data/ward', headers=headers, json=json_ward)
	dataAPI_ward = r.json()
	for i in range(len(dataAPI_province['data'])):
			#print(dataAPI_province['data'][i].get("ProvinceID"))
		if (dataAPI_province['data'][i].get("ProvinceID"))==ProvinceName:
			province = dataAPI_province['data'][i].get("ProvinceName")
	for i in range(len(dataAPI_district['data'])):
		#print(dataAPI_province['data'][i].get("ProvinceID"))
		if (dataAPI_district['data'][i].get("DistrictID"))==DistrictName:
			district = dataAPI_district['data'][i].get("DistrictName")
	for i in range(len(dataAPI_ward['data'])):
		#print(dataAPI_ward['data'][i].get("WardCode"))
		if dataAPI_ward['data'][i].get("WardCode")==WardName:
			ward = dataAPI_ward['data'][i].get("WardName") 
	# địa chỉ gửi hàng
	for i in range(len(dataAPI_province['data'])):
		if (dataAPI_province['data'][i].get("ProvinceID"))==city_id:
			pick_province = dataAPI_province['data'][i].get("ProvinceName")
	json_district_shop = {"province_id": city_id}
	r = requests.get('https://online-gateway.ghn.vn/shiip/public-api/master-data/district', headers=headers, json=json_district_shop)
	json_district_shop = r.json()

	for i in range(len(json_district_shop['data'])):
		if json_district_shop['data'][i].get("DistrictID") == district_id:
			pick_district = json_district_shop['data'][i].get("DistrictName")
	print(pick_province)
	print(pick_district)
	
	# tính giá trị đơn hàng
	#print(int(total*1000000))
	#temp = int(total*1000000)
	# if temp < 20000000:
	# 	insurance_fee = temp
	# else:
	# 	insurance_fee = 20000000
	# print(insurance_fee)
	# tính giá cước
	insurance_fee = 3000000
	weight = weight*quantity
	headers={'Content-Type':'application/json', 'Token': mytoken_ghtk}
	json = {
		"pick_province": pick_province,
		"pick_district": pick_district,
		"province": province,
		"district": district,
		"ward": ward,
		"weight": weight,
		"value": insurance_fee,
		"transport": "fly",
		"tags": [1]
	}
	# "tags": [1] Gắn nhãn dễ vỡ cho đơn hàng. Truyền giá trị 1 vào mảng tags nếu là đơn dễ vỡ
	r = requests.get('https://services.giaohangtietkiem.vn/services/shipment/fee?', headers=headers, json=json)
	dataAPI_transport_fee = r.json()
		
	transport_fee = 0
	transport_fee = dataAPI_transport_fee['fee']['fee']
	total_order = int(float(total)*1000000)
	# phí vận chuyển
	if request.POST.get('action') == 'post':
		ghtk = request.POST.get('ghtk')
		#print(ghtk)
		total_new = total_order + transport_fee
		total_order = format_number(total_order, locale='de_DE')
		transport_fee = format_number(transport_fee, locale='de_DE')
		total_new = format_number(total_new, locale='de_DE')
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
	for i in storeaddress:
		adress_id = int(i.city)			#không cần dùng
		shop_id = i.ShopID_GHN
		district_id = int(i.district)
		length = i.length
		width = i.width
		height = i.height
		weight = i.weight
		
	current_user = request.user
	shopcart = ShopCart.objects.filter(user_id=current_user.id)
	# gia tri order producted
	total = 0
	for rs in shopcart:
		total += rs.variant.price * rs.quantity
	#print(int(total*1000000))
	
	#so luong order producted
	quantity = 0
	for rs in shopcart:
		quantity += rs.quantity
	# Xử lí API GHN
	
	# tính hình thức vận chuyển
	to_district = int(request.POST.get('DistrictName'))
	#print(district_id)
	#print(to_district)
	headers={'Content-Type':'application/json', 'Token': mytoken}
	json_district = {
		"shop_id": shop_id,
		"from_district": district_id,
		"to_district": to_district
	}
	r = requests.get('https://online-gateway.ghn.vn/shiip/public-api/v2/shipping-order/available-services', headers=headers, json=json_district)
	dataAPI_thongtin = r.json()
	ServiceID_API = []
	for i in dataAPI_thongtin['data']:
		ServiceID_API.append(i['service_type_id'])

	for i in range(len(ServiceID_API)):
		#print(ServiceID_API[i], type(ServiceID_API[i]))
		if ServiceID_API[i]==2:
			service_type_id = 2
		else:
			service_type_id = 1

	to_ward_code = request.POST.get('WardName')
	# tính giá trị đơn hàng
	#print(int(total*1000000))
	temp = int(total*1000000)
	if temp < 10000000:
		insurance_fee = temp
	else:
		insurance_fee = 10000000
	#print(insurance_fee)
	#print(to_ward_code, type(to_ward_code))
	# tính giá cước

	weight = weight*quantity
	json_district = {
		"from_district_id": district_id,			# gửi từ
		'service_type_id': service_type_id,			# hình thức vận chuyển
		"to_district_id": to_district,				# quận huyện
		"to_ward_code": to_ward_code,				# đến xã, phường
		"height": height,							# chiều cao đơn hàng								
		"length":length,							# Chiều dài đơn hàng
		"weight": weight,							# khối lượng của đơn hàng
		"width":width,								# chiều rộng của đơn hàng
		"insurance_fee": insurance_fee,				# giá trị đơn hàng
		}
	r = requests.get('https://online-gateway.ghn.vn/shiip/public-api/v2/shipping-order/fee', headers=headers, json=json_district)
	dataAPI_transport_fee = r.json()
	
	transport_fee = 0
	transport_fee = int(dataAPI_transport_fee['data']['total'])
	total_order = int(float(total)*1000000)
	# tempabc = float(total_order)
	# tempabc = tempabc/1000000
	# print(tempabc)
	#transport_fee = 0  # phí vận chuyển
	if request.POST.get('action') == 'post':
		ghtk = request.POST.get('ghn')
		#print(ghtk)
		total_new = total_order + transport_fee
		total_order = format_number(total_order, locale='de_DE')
		transport_fee = format_number(transport_fee, locale='de_DE')
		total_new = format_number(total_new, locale='de_DE')
		context = {
			'ghtk': ghtk,
			'total_order': total_order,			# tổng tiền order
			'transport_fee': transport_fee,
			'total_new': total_new  # tổng tiền thanh toán
		}
		data = {'rendered_table': render_to_string('checkout/total-online.html', context=context)}
		return JsonResponse(data)
	return JsonResponse(data)