from apps.product.models import Category, Product, Variants
from apps.order.models import ShopCart, ShopCartForm, OrderForm, Order, OrderProduct, OrderWaitingPayment
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
from babel.numbers import format_number
from apps.vnpay_python.forms import PaymentForm
from apps.vnpay_python.vnpay import vnpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import requests
from django.contrib.auth.decorators import login_required

mytoken = "62045ed5-d43f-11eb-81f5-a267211ac77c"
mytoken_ghtk = "D85E94443Fe9647029c79A1E45d1837e35C7Cfec"
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
	# địa chỉ cửa hàng
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
	
	if request.method == 'POST':  # if there is a post
		form = OrderForm(request.POST)
		if form.is_valid():
			# Send Credit card to bank,  If the bank responds ok, continue, if not, show the error
			# ..............
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
			
			# event tinh tien giao hang
			giaohang = request.POST.get('delivery')
			if giaohang=='Giao hàng tiết kiệm':
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
				total_new = total_order + transport_fee   
			elif giaohang=='Giao hàng nhanh':
				to_district = int(request.POST.get('DistrictName'))
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
			form_Payment = PaymentForm(request.POST)
			if form_Payment.is_valid():
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
				vnp.requestData['vnp_Amount'] = total_new*100
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
				# gán giá trị tạm thời của post để kiểm tra thanh toán
				temp_user_id = current_user.id
				temp_ordercode = order_id
				temp_first_name = form.cleaned_data['first_name']
				temp_last_name = form.cleaned_data['last_name']
				temp_phone = form.cleaned_data['phone']
				temp_province = Province
				temp_district = District
				temp_ward = Ward
				temp_address = form.cleaned_data['address']
				temp_total = total_new
				temp_status_pay = 'Đã thanh toán'
				temp_delivery = giaohang
				temp_transport_fee = transport_fee
				temp_ip = request.META.get('REMOTE_ADDR')
				order_temp = OrderWaitingPayment()
				order_temp.user_id = temp_user_id
				order_temp.code = temp_ordercode
				order_temp.first_name = temp_first_name
				order_temp.last_name = temp_last_name
				order_temp.phone = temp_phone
				order_temp.province = temp_province
				order_temp.district = temp_district
				order_temp.ward = temp_ward
				order_temp.address = temp_address
				order_temp.total = temp_total
				order_temp.status_pay = temp_status_pay
				order_temp.delivery = temp_delivery
				order_temp.transport_fee = temp_transport_fee
				order_temp.ip = temp_ip
				order_temp.save()
				print(order_temp)
				
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
	#print(total)
	price = int(total * 1000)*1000
	#price = format_number(price, locale='de_DE')
	price_ui = format_number(price, locale='de_DE')
	#print(price)
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
		'price_ui': price_ui,
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
		city_id = int(i.city)
	
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
				total_new = total_order + transport_fee
			elif giaohang=='Giao hàng nhanh':
				to_district = int(request.POST.get('DistrictName'))
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
					if ServiceID_API[i]==2:
						service_type_id = 2
					else:
						service_type_id = 1

				to_ward_code = request.POST.get('WardName')
				# tính giá trị đơn hàng
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



