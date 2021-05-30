from django.http.response import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
# Create your views here.
from apps.order.models import ShopCart, ShopCartForm, OrderForm, Order
from django.contrib.auth.decorators import login_required
from apps.account.models import UserProfile
from apps.product.models import Category, Product, Variants
from django.shortcuts import render


@login_required(login_url='/account/login')# Check login
def addtoshopcart(request,id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  
    product= Product.objects.get(pk=id)

    if product.variant != 'None':
        variantid = request.POST.get('variantid')  
        checkinvariant = ShopCart.objects.filter(variant_id=variantid, user_id=current_user.id)  
        if checkinvariant:
            control = 1 
        else:
            control = 0 
    else:
        checkinproduct = ShopCart.objects.filter(product_id=id, user_id=current_user.id) 
        if checkinproduct:
            control = 1 
        else:
            control = 0 

    if request.method == 'POST':  
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control==1: 
                if product.variant == 'None':
                    data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
                else:
                    data = ShopCart.objects.get(product_id=id, variant_id=variantid, user_id=current_user.id)
                data.quantity += form.cleaned_data['quantity']
                data.save()  
            else : 
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.variant_id = variantid
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, "Thêm sản phẩm thành công")
        return HttpResponseRedirect(url)

    else: 
        if control == 1:  
            data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
            data.quantity += 1
            data.save()  
        else:  
            data = ShopCart() 
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.variant_id =None
            data.save()  
        messages.success(request, "Thêm sản phẩm thành công")
        return HttpResponseRedirect(url)


def shopcart(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.variant.price * rs.quantity
    quantity = 0
    for rs in shopcart:
        quantity += rs.quantity
    context = {
        'shopcart': shopcart,
        'category': category,
        'total': total,
        'quantity': quantity
    }
    return render(request, 'order/order-detail.html', context)


@login_required(login_url='/account/login')
def deletefromcart(request, id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Xóa sản phẩm thành công.")
    return HttpResponseRedirect("/order")


@login_required(login_url='/account/login')
def orderproduct(request):
	category = Category.objects.all()
	current_user = request.user
	shopcart = ShopCart.objects.filter(user_id=current_user.id)
	total = 0
	for rs in shopcart:
		total += rs.variant.price*rs.quantity
	if request.method =='POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			data = Order()
			data.first_name = form.cleaned_data['first_name']
			data.last_name = form.cleaned_data['last_name']
			data.address = form.cleaned_data['address']
			# data.city = form.cleaned_data['city']
			data.phone = form.cleaned_data['phone']
			data.user_id = current_user.id
			data.total = total
			data.ip = request.META.get('REMOTE_ADDR')
			ordercode = get_random_string(5).upper()
			data.save()
	return HttpResponse("Thanh toán")

