import urllib.request
import urllib.parse
from datetime import datetime
from django.core.serializers import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from apps.product.models import Category
from apps.vnpay_python.forms import PaymentForm
from apps.vnpay_python.vnpay import vnpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from apps.order.models import ShopCart, ShopCartForm, OrderForm, Order, OrderProduct, OrderWaitingPayment
from apps.product.models import Category, Product, Variants
from django.utils.crypto import get_random_string
from django.contrib import messages
import stripe
import urllib.request
import urllib.parse
from datetime import datetime
from apps.home.models import StoreAddress
from django.core.serializers import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect


def index(request):
	return render(request, "vnpay_python/index.html", {"title": "Danh sách demo"})


#@csrf_exempt
def payment(request):
	print("hello1")
	if request.method == 'POST':
		print("hello2")
		# Process input data and build url payment
		form = PaymentForm(request.POST)
		if form.is_valid():
			print("hello3")
			order_type = form.cleaned_data['order_type']
			order_id = form.cleaned_data['order_id']
			amount = form.cleaned_data['amount']
			order_desc = form.cleaned_data['order_desc']
			bank_code = form.cleaned_data['bank_code']
			language = form.cleaned_data['language']
			ipaddr = get_client_ip(request)
			# Build URL Payment
			vnp = vnpay()
			vnp.requestData['vnp_Version'] = '2.0.0'
			vnp.requestData['vnp_Command'] = 'pay'
			vnp.requestData['vnp_TmnCode'] = settings.VNPAY_TMN_CODE
			vnp.requestData['vnp_Amount'] = amount * 100
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
			print(vnpay_payment_url)
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
			print("hello6")
			print("Form input not validate")
	else:
		print("hello7")
		return render(request, "vnpay_python/payment.html", {"title": "Thanh toán", "price": request.GET["price"]})


def payment_ipn(request):
	inputData = request.GET
	if inputData:
		vnp = vnpay()
		vnp.responseData = inputData.dict()
		order_id = inputData['vnp_TxnRef']
		amount = inputData['vnp_Amount']
		order_desc = inputData['vnp_OrderInfo']
		vnp_TransactionNo = inputData['vnp_TransactionNo']
		vnp_ResponseCode = inputData['vnp_ResponseCode']
		vnp_TmnCode = inputData['vnp_TmnCode']
		vnp_PayDate = inputData['vnp_PayDate']
		vnp_BankCode = inputData['vnp_BankCode']
		vnp_CardType = inputData['vnp_CardType']
		if vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
			# Check & Update Order Status in your Database
			# Your code here
			firstTimeUpdate = True
			if firstTimeUpdate:
				if vnp_ResponseCode == '00':
					print('Payment Success. Your code implement here')
				else:
					print('Payment Error. Your code implement here')

				# Return VNPAY: Merchant update success
				result = JsonResponse({'RspCode': '00', 'Message': 'Confirm Success'})
			else:
				# Already Update
				result = JsonResponse({'RspCode': '02', 'Message': 'Order Already Update'})

		else:
			# Invalid Signature
			result = JsonResponse({'RspCode': '97', 'Message': 'Invalid Signature'})
	else:
		result = JsonResponse({'RspCode': '99', 'Message': 'Invalid request'})

	return result


def payment_return(request):
	category = Category.objects.all()
	current_user = request.user
	shopcart = ShopCart.objects.filter(user_id=current_user.id)
	total = 0
	for rs in shopcart:
		total += rs.variant.price * rs.quantity
	quantity = 0
	for rs in shopcart:
		quantity += rs.quantity
	inputData = request.GET
	if inputData:
		vnp = vnpay()
		vnp.responseData = inputData.dict()
		order_id = inputData['vnp_TxnRef']
		amount = int(inputData['vnp_Amount']) / 100
		order_desc = inputData['vnp_OrderInfo']
		vnp_TransactionNo = inputData['vnp_TransactionNo']
		vnp_ResponseCode = inputData['vnp_ResponseCode']
		vnp_TmnCode = inputData['vnp_TmnCode']
		vnp_PayDate = inputData['vnp_PayDate']
		vnp_BankCode = inputData['vnp_BankCode']
		vnp_CardType = inputData['vnp_CardType']
		if vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
			if vnp_ResponseCode == "00":
				total = 0
				quantity = 0
				order_temp_data = OrderWaitingPayment.objects.filter(user_id=current_user.id)
				print(order_id)

				for order_temp in order_temp_data:
					print(order_temp.code)
					if order_temp.code == order_id:
						data = Order()
						data.user_id = order_temp.user_id
						data.first_name = order_temp.first_name
						data.last_name = order_temp.last_name
						data.phone = order_temp.phone
						data.province = order_temp.province
						data.district = order_temp.district
						data.ward = order_temp.ward
						data.address = order_temp.address
						data.total = order_temp.total
						data.status_pay = order_temp.status_pay
						data.delivery = order_temp.delivery
						data.transport_fee = order_temp.transport_fee	
						data.ip = order_temp.ip
						data.code = order_temp.code
						data.save()
						shopcart = ShopCart.objects.filter(user_id=order_temp.user)
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
						ShopCart.objects.filter(user_id=current_user.id).delete()
						print("Luu thong tin thanh cong")
				return render(request, "vnpay_python/payment_return.html", {"title": "Kết quả thanh toán",
																"result": "Thành công", "order_id": order_id,
																"amount": amount,
																"order_desc": order_desc,
																"category": category,
																"total": total,
																"quantity": quantity,
																"vnp_TransactionNo": vnp_TransactionNo,
																"vnp_ResponseCode": vnp_ResponseCode})
			else:
				return render(request, "vnpay_python/payment_return.html", {"title": "Kết quả thanh toán",
																"result": "Lỗi", "order_id": order_id,
																"amount": amount,
																"order_desc": order_desc,
																"category": category,
																"total": total,
																"quantity": quantity,
																"vnp_TransactionNo": vnp_TransactionNo,
																"vnp_ResponseCode": vnp_ResponseCode})
		else:
			return render(request, "vnpay_python/payment_return.html",
							{"title": "Kết quả thanh toán", "result": "Lỗi", "order_id": order_id, "amount": amount,
							"order_desc": order_desc, "vnp_TransactionNo": vnp_TransactionNo,"category": category,
							"total": total,"quantity": quantity,"vnp_ResponseCode": vnp_ResponseCode, "msg": "Sai checksum"})
	else:
		return render(request, "vnpay_python/payment_return.html", {"title": "Kết quả thanh toán", "result": ""})


def query(request):
	if request.method == 'GET':
		return render(request, "vnpay_python/query.html", {"title": "Kiểm tra kết quả giao dịch"})
	else:
		# Add paramter
		vnp = vnpay()
		vnp.requestData = {}
		vnp.requestData['vnp_Command'] = 'querydr'
		vnp.requestData['vnp_Version'] = '2.0.0'
		vnp.requestData['vnp_TmnCode'] = settings.VNPAY_TMN_CODE
		vnp.requestData['vnp_TxnRef'] = request.POST['order_id']
		vnp.requestData['vnp_OrderInfo'] = 'Kiem tra ket qua GD OrderId:' + request.POST['order_id']
		vnp.requestData['vnp_TransDate'] = request.POST['trans_date']  # 20150410063022
		vnp.requestData['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')  # 20150410063022
		vnp.requestData['vnp_IpAddr'] = get_client_ip(request)
		requestUrl = vnp.get_payment_url(settings.VNPAY_API_URL, settings.VNPAY_HASH_SECRET_KEY)
		responseData = urllib.request.urlopen(requestUrl).read().decode()
		print('RequestURL:' + requestUrl)
		print('VNPAY Response:' + responseData)
		data = responseData.split('&')
		for x in data:
			tmp = x.split('=')
			if len(tmp) == 2:
				vnp.responseData[tmp[0]] = urllib.parse.unquote(tmp[1]).replace('+', ' ')

		print('Validate data from VNPAY:' + str(vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY)))
		return render(request, "vnpay_python/query.html", {"title": "Kiểm tra kết quả giao dịch", "data": vnp.responseData})


def refund(request):
	return render(request, "vnpay_python/refund.html", {"title": "Gửi yêu cầu hoàn tiền"})


def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip
