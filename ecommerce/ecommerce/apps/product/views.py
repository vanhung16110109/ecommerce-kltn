from django.shortcuts import render
from apps.product.models import Category, Product, Images, CommentForm, Comment, Variants
from django.http.response import HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from apps.order.models import ShopCart
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request
from django.template.loader import render_to_string
import json


def category_products(request, id, slug):
    category = Category.objects.all()
    products = Product.objects.filter(category_id = id)
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity
    quantity = 0
    for rs in shopcart:
        quantity += rs.quantity
    context = {
        'category':category,
        'products': products,
		'total': total,
        'quantity': quantity,
    }
    return render(request, 'product/category_products.html',context)


def addcomment(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            data = Comment()
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.product_id = id
            current_user = request.user
            data.user_id = current_user.id
            data.save()
            messages.success(request, "Cảm ơn bạn đã gửi bình luận và đánh giá cho chúng tôi.")
            return HttpResponseRedirect(url)

    return HttpResponseRedirect(url)


def product_detail(request, id, slug):
	query = request.GET.get('q')
	current_user = request.user
	shopcart = ShopCart.objects.filter(user_id=current_user.id)
	total = 0
	for rs in shopcart:
		total += rs.product.price * rs.quantity
	quantity = 0
	for rs in shopcart:
		quantity += rs.quantity
	category = Category.objects.all()
	product = Product.objects.get(pk=id)
	images = Images.objects.filter(product_id=id)
	comments = Comment.objects.filter(product_id=id)
	# details = DetailsProduct.objects.filter(product_id=id)
	context = {
        'comments': comments,
        'product': product,
        'category': category,
        'images': images,
		'total': total,
        'quantity': quantity,
		# 'deta': details,
    }
	if product.variant !="None": # Product have variants
		if request.method == 'POST': #if we select color
			variant_id = request.POST.get('variantid')
			variant = Variants.objects.get(id=variant_id) #selected product by click color radio
			colors = Variants.objects.filter(product_id=id,size_id=variant.size_id)
			sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id',[id])
			query += variant.title+' Size:' +str(variant.size) +' Color:' +str(variant.color)
		else:
			variants = Variants.objects.filter(product_id=id)
			colors = Variants.objects.filter(product_id=id,size_id=variants[0].size_id )
			sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id',[id])
			variant =Variants.objects.get(id=variants[0].id)
		context.update({'sizes': sizes, 'colors': colors,
                        'variant': variant,'query': query
                        })
	return render(request, 'product/product-detail.html', context)


def ajaxcolor(request):
    data = {}
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = Variants.objects.filter(product_id=productid, size_id=size_id)
        context = {
            'size_id': size_id,
            'productid': productid,
            'colors': colors,
        }
        data = {'rendered_table': render_to_string('product/color_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)