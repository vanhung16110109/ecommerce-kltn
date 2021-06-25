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

from django.core.serializers import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect

from apps.vnpay_python.forms import PaymentForm
from apps.vnpay_python.vnpay import vnpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = "sk_test_51J1vyDAGJ7lQptUOWAiE572OEq7GeThZxmZVMqakGn9nQubgtdCoSw4PxE7Qjg4zrKBzZTXsIfWKtR04Lr7BkMax00VJxyICNk"


# Create your views here.
#checkout online
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
    ordercode = get_random_string(5).upper() # random cod
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
            # data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            #ordercode = get_random_string(5).upper() # random cod
            data.code =  ordercode
            data.status_pay = 'Đã thanh toán'
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
            # # messages.success(request, "Đơn hàng của bạn đã được hoàn thành. Cảm ơn bạn")
            # return render(request, 'order/Order_Completed.html',context)
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
            # ShopCart.objects.filter(user_id=current_user.id).delete() # Clear & Delete shopcart
            # # request.session['cart_items']=0
            # total = 0
            # quantity = 0
            # context = {
			# 	'total': total,
			# 	'quantity': quantity,
			# 	'ordercode':ordercode,'category': category
			# }
            # return render(request, 'order/Order_Completed.html',context)
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
    }
    return render(request, 'checkout/checkout-online.html', context)


#checkout_offline
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
    if request.method == 'POST':  # if there is a post
        form = OrderForm(request.POST)
        #return HttpResponse(request.POST.items())
        if form.is_valid():
            # Send Credit card to bank,  If the bank responds ok, continue, if not, show the error
            # ..............

            data = Order()
            data.first_name = form.cleaned_data['first_name'] #get product quantity from form
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            # data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            #ordercode= get_random_string(5).upper() # random cod
            data.code =  ordercode
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
				'ordercode':ordercode,'category': category
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
    }
    return render(request, 'checkout/checkout-offline.html', context)



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
