from apps.product.models import Category, Product, Variants
from apps.order.models import ShopCart, ShopCartForm, OrderForm, Order, OrderProduct
from apps.account.models import UserProfile
from django.utils.crypto import get_random_string
from django.shortcuts import render
from django.contrib import messages
import stripe
import urllib.request
import urllib.parse
from datetime import datetime
from apps.home.models import StoreAddress
from django.core.serializers import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect

from apps.vnpay_python.forms import PaymentForm
from apps.vnpay_python.vnpay import vnpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import requests
from django.contrib.auth.decorators import login_required

mytoken = "62045ed5-d43f-11eb-81f5-a267211ac77c"

stripe.api_key = "sk_test_51J1vyDAGJ7lQptUOWAiE572OEq7GeThZxmZVMqakGn9nQubgtdCoSw4PxE7Qjg4zrKBzZTXsIfWKtR04Lr7BkMax00VJxyICNk"


# Create your views here.
#checkout online
@login_required(login_url='/account/login')
def checkout_online(request):
	category = Category.objects.all()
	product = Product.objects.all()
	current_user = request.user
	shopcart = ShopCart.objects.filter(user_id=current_user.id)
	total = 0
	for rs in shopcart:
		total += rs.variant.price * rs.quantity
	quantity = 0
	for rs in shopcart:
		quantity += rs.quantity
	storeaddress = StoreAddress.objects.filter(id=1)
	for i in storeaddress:
		adress_id = int(i.city)
	ordercode = get_random_string(5).upper() # random cod
	headers={'Content-Type':'application/json', 'Token': mytoken}
	r = requests.get('https://online-gateway.ghn.vn/shiip/public-api/master-data/province', headers=headers)
	dataAPI_province = r.json()
	if request.method == 'POST':  # if there is a post
		form = OrderForm(request.POST)
		form_Payment = PaymentForm(request.POST)
		#return HttpResponse(request.POST.items())
		if form.is_valid():
			# Send Credit card to bank,  If the bank responds ok, continue, if not, show the error
			# ..............
			
			data = Order()
			data.first_name = form.cleaned_data['first_name'] #get product quantity from form
			data.last_name = form.cleaned_data['last_name']
			data.address = form.cleaned_data['address']
			#get data location
			ProvinceName = int(request.POST.get('ProvinceName'))        #get id
			DistrictName = int(request.POST.get('DistrictName'))
			WardName = int(request.POST.get('WardName'))
			json_district = {"province_id": ProvinceName}
			r = requests.get('https://online-gateway.ghn.vn/shiip/public-api/master-data/district', headers=headers, json=json_district)
			dataAPI_district = r.json()
			json_ward = {"district_id": DistrictName}
			r = requests.get('https://online-gateway.ghn.vn/shiip/public-api/master-data/ward', headers=headers, json=json_ward)
			dataAPI_ward = r.json()
			#print(dataAPI_ward)
			for i in range(len(dataAPI_province['data'])):
				#print(dataAPI_province['data'][i].get("ProvinceID"))
				if (dataAPI_province['data'][i].get("ProvinceID"))==ProvinceName:
					Province = dataAPI_province['data'][i].get("ProvinceName")
			for i in range(len(dataAPI_district['data'])):
				#print(dataAPI_province['data'][i].get("ProvinceID"))
				if (dataAPI_district['data'][i].get("DistrictID"))==DistrictName:
					District = dataAPI_district['data'][i].get("DistrictName")
			for i in range(len(dataAPI_ward['data'])):
				#print(dataAPI_ward['data'][i].get("WardCode"))
				if int(dataAPI_ward['data'][i].get("WardCode"))==WardName:
					Ward = dataAPI_ward['data'][i].get("WardName")    
			# print(Province)
			# print(District)
			# print(Ward)
			data.province = Province
			data.district = District
			data.ward = Ward
			data.phone = form.cleaned_data['phone']
			data.user_id = current_user.id
			#event tinh tien giao
			giaohang = request.POST.get('delivery')
			if giaohang=='Giao hàng tiết kiệm':
				print('Có')
				if adress_id == ProvinceName:
					transport_fee = 30
					total_new = (total*1000 + 30)/1000
				else:
					transport_fee = 40
					total_new = (total*1000 + 40)/1000
			elif giaohang=='Giao hàng nhanh':
				if adress_id == ProvinceName:
					transport_fee = 37
					total_new = (total*1000 + 37)/1000
				else:
					transport_fee = 47
					total_new = (total*1000 + 47)/1000                             
			data.total = total_new
			data.ip = request.META.get('REMOTE_ADDR')
			#ordercode = get_random_string(5).upper() # random cod
			data.code =  ordercode
			data.status_pay = 'Đã thanh toán'
			data.save()

			for rs in shopcart:
				detail = OrderProduct()
				detail.order_id     = data.id # Order Id
				detail.product_id   = rs.product_id
				detail.user_id      = current_user.id
				detail.quantity     = rs.quantity
				if rs.product.variant == 'None':
					detail.price    = rs.product.price
				else:
					detail.price = rs.variant.price
				detail.variant_id   = rs.variant_id
				# detail.amount        = rs.amount
				detail.amount       = rs.varamount

				detail.save()
				# ***Reduce quantity of sold product from Amount of Product
				if rs.product.variant == 'None':
					product = Product.objects.get(id=rs.product_id)
					product.amount -= rs.quantity
					product.save()
				else:
					#variant = Variants.objects.get(id=rs.product_id)
					variant = Variants.objects.get(id=rs.variant_id)
					variant.quantity -= rs.quantity
					variant.save()
				#************ <> *****************
			# # messages.success(request, "Đơn hàng của bạn đã được hoàn thành. Cảm ơn bạn")
			# return render(request, 'order/Order_Completed.html',context)
			transport_fee = transport_fee*100000
			if form_Payment.is_valid():
				print("hello3")
				order_type = form_Payment.cleaned_data['order_type']
				order_id = form_Payment.cleaned_data['order_id']
				amount = form_Payment.cleaned_data['amount']
				order_desc = form_Payment.cleaned_data['order_desc']
				bank_code = form_Payment.cleaned_data['bank_code']
				language = form_Payment.cleaned_data['language']
				ipaddr = get_client_ip(request)
				# Build URL Payment
				vnp = vnpay()
				vnp.requestData['vnp_Version'] = '2.0.0'
				vnp.requestData['vnp_Command'] = 'pay'
				vnp.requestData['vnp_TmnCode'] = settings.VNPAY_TMN_CODE
				vnp.requestData['vnp_Amount'] = amount * 100 + transport_fee
				vnp.requestData['vnp_CurrCode'] = 'VND'
				vnp.requestData['vnp_TxnRef'] = order_id
				vnp.requestData['vnp_OrderInfo'] = order_desc
				vnp.requestData['vnp_OrderType'] = order_type
				# Check language, default: vn
				if language and language != '':
					vnp.requestData['vnp_Locale'] = language
				else:
					vnp.requestData['vnp_Locale'] = 'vn'
					# Check bank_code, if bank_code is empty, customer will be selected bank on VNPAY
				if bank_code and bank_code != "":
					vnp.requestData['vnp_BankCode'] = bank_code

				vnp.requestData['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')  # 20150410063022
				vnp.requestData['vnp_IpAddr'] = ipaddr
				vnp.requestData['vnp_ReturnUrl'] = settings.VNPAY_RETURN_URL
				vnpay_payment_url = vnp.get_payment_url(settings.VNPAY_PAYMENT_URL, settings.VNPAY_HASH_SECRET_KEY)
				#print(vnpay_payment_url)
				ShopCart.objects.filter(user_id=current_user.id).delete()
				if request.is_ajax():
					print("hello4")
					# Show VNPAY Popup
					result = JsonResponse({'code': '00', 'Message': 'Init Success', 'data': vnpay_payment_url})
					print("hello5 === ", result)
					return result
				else:
					print("hello5")
					# Redirect to VNPAY
					return redirect(vnpay_payment_url)
						
		else:
			messages.warning(request, form.errors)
			return HttpResponseRedirect("/order/orderproduct")

	form = OrderForm()
	profile = UserProfile.objects.get(user_id=current_user.id)
	print(total)
	price = int(total * 1000)*1000
	print(price)
	context = {
		'shopcart': shopcart,
		'category': category,
		'total': total,
		'price': price,
		'quantity': quantity,
		'form': form,
		'profile': profile,
		'ordercode': ordercode,
		'dataAPI_province': dataAPI_province,
	}
	return render(request, 'checkout/checkout-online.html', context)


#checkout_offline
@login_required(login_url='/account/login')
def checkout_offline(request):
	category = Category.objects.all()
	product = Product.objects.all()
	current_user = request.user
	shopcart = ShopCart.objects.filter(user_id=current_user.id)
	total = 0
	for rs in shopcart:
		total += rs.variant.price * rs.quantity
	quantity = 0
	for rs in shopcart:
		quantity += rs.quantity
	ordercode= get_random_string(5).upper()
	headers={'Content-Type':'application/json', 'Token': mytoken}
	r = requests.get('https://online-gateway.ghn.vn/shiip/public-api/master-data/province', headers=headers)
	dataAPI_province = r.json()
	# địa chỉ cửa hàng
	storeaddress = StoreAddress.objects.filter(id=1)
	for i in storeaddress:
		adress_id = int(i.city)			#không cần dùng
		shop_id = i.ShopID_GHN
		district_id = int(i.district)
		length = i.length
		width = i.width
		height = i.height
		weight = i.weight
	
	if request.method == 'POST':  # if there is a post
		form = OrderForm(request.POST)
		if form.is_valid():
			# Send Credit card to bank,  If the bank responds ok, continue, if not, show the error
			# ..............

			data = Order()
			data.first_name = form.cleaned_data['first_name'] #get product quantity from form
			data.last_name = form.cleaned_data['last_name']
			ProvinceName = int(request.POST.get('ProvinceName'))        #get id
			DistrictName = int(request.POST.get('DistrictName'))
			WardName = int(request.POST.get('WardName'))
			# print(WardName)
			
			json_district = {"province_id": ProvinceName}
			r = requests.get('https://online-gateway.ghn.vn/shiip/public-api/master-data/district', headers=headers, json=json_district)
			dataAPI_district = r.json()
			json_ward = {"district_id": DistrictName}
			r = requests.get('https://online-gateway.ghn.vn/shiip/public-api/master-data/ward', headers=headers, json=json_ward)
			dataAPI_ward = r.json()
			# get ID Province, District, Ward
			for i in range(len(dataAPI_province['data'])):
				#print(dataAPI_province['data'][i].get("ProvinceID"))
				if (dataAPI_province['data'][i].get("ProvinceID"))==ProvinceName:
					Province = dataAPI_province['data'][i].get("ProvinceName")
			for i in range(len(dataAPI_district['data'])):
				#print(dataAPI_province['data'][i].get("ProvinceID"))
				if (dataAPI_district['data'][i].get("DistrictID"))==DistrictName:
					District = dataAPI_district['data'][i].get("DistrictName")
			for i in range(len(dataAPI_ward['data'])):
				#print(dataAPI_ward['data'][i].get("WardCode"))
				if int(dataAPI_ward['data'][i].get("WardCode"))==WardName:
					Ward = dataAPI_ward['data'][i].get("WardName")    
			# gán dữ liệu
			data.province = Province
			data.district = District
			data.ward = Ward
			data.address = form.cleaned_data['address']
			data.phone = form.cleaned_data['phone']
			data.user_id = current_user.id
			# event tinh tien giao hang
			giaohang = request.POST.get('delivery')
			if giaohang=='Giao hàng tiết kiệm':
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
				total_new = total_order + transport_fee
			elif giaohang=='Giao hàng nhanh':
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
				total_new = total_order + transport_fee       
			#total_new = (total*1000 + 47)/1000	
			data.total = total_new
			data.ip = request.META.get('REMOTE_ADDR')
			#ordercode= get_random_string(5).upper() # random cod
			data.code =  ordercode
			data.delivery = giaohang
			data.transport_fee = transport_fee
			data.save() #

			for rs in shopcart:
				detail = OrderProduct()
				detail.order_id     = data.id # Order Id
				detail.product_id   = rs.product_id
				detail.user_id      = current_user.id
				detail.quantity     = rs.quantity
				if rs.product.variant == 'None':
					detail.price    = rs.product.price
				else:
					detail.price = rs.variant.price
				detail.variant_id   = rs.variant_id
				# detail.amount        = rs.amount
				detail.amount       = rs.varamount

				detail.save()
				# ***Reduce quantity of sold product from Amount of Product
				if rs.product.variant == 'None':
					product = Product.objects.get(id=rs.product_id)
					product.amount -= rs.quantity
					product.save()
				else:
					#variant = Variants.objects.get(id=rs.product_id)
					variant = Variants.objects.get(id=rs.variant_id)
					variant.quantity -= rs.quantity
					variant.save()
				#************ <> *****************

			ShopCart.objects.filter(user_id=current_user.id).delete() # Clear & Delete shopcart
			total = 0
			quantity = 0
			context = {
				'total': total,
				'quantity': quantity,
				'ordercode':ordercode,'category': category,
				'dataAPI_province': dataAPI_province,
			}
			# messages.success(request, "Đơn hàng của bạn đã được hoàn thành. Cảm ơn bạn")
			return render(request, 'order/Order_Completed.html',context)
		else:
			messages.warning(request, form.errors)
			return HttpResponseRedirect("/order/orderproduct")

	form= OrderForm()
	profile = UserProfile.objects.get(user_id=current_user.id)
	context = {
		'shopcart': shopcart,
		'category': category,
		'total': total,
		'quantity': quantity,
		'form': form,
		'profile': profile,
		'ordercode': ordercode,
		'dataAPI_province': dataAPI_province,
	}
	return render(request, 'checkout/checkout-offline.html', context)



def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip


