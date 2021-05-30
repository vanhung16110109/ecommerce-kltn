from django.shortcuts import render
from apps.product.models import Category, Product, Variants
from apps.order.models import ShopCart, ShopCartForm, OrderForm, Order, OrderProduct
from apps.account.models import UserProfile
from django.utils.crypto import get_random_string
from django.shortcuts import render
from django.contrib import messages
# Create your views here.
#checkout online
def checkout_online(request):
    return render(request, 'checkout/checkout-online.html', {})


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
            ordercode= get_random_string(5).upper() # random cod
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
            request.session['cart_items']=0
            messages.success(request, "Your Order has been completed. Thank you ")
            return render(request, 'Order_Completed.html',{'ordercode':ordercode,'category': category})
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
    }
    return render(request, 'checkout/checkout-offline.html', context)




