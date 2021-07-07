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
	product_all = Product.objects.all()
	total = 0
	for rs in shopcart:
		total += rs.variant.price * rs.quantity
	quantity = 0
	for rs in shopcart:
		quantity += rs.quantity
	context = {
		'category':category,
		'products': products,
		'total': total,
		'quantity': quantity,
		'product_all': product_all,
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
		total += rs.variant.price * rs.quantity
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
			variant = Variants.objects.get(id=variants[0].id)
		context.update({'sizes': sizes, 'colors': colors,
						'variant': variant,'query': query
						})
	return render(request, 'product/product-detail.html', context)


def ajaxcolor(request):
	data = {}
	if request.POST.get('action') == 'post':
		size_id = request.POST.get('size')
		productid = request.POST.get('productid')
		print(size_id)
		print(productid)
		colors = Variants.objects.filter(product_id=productid, size_id=size_id)
		context = {
			'size_id': size_id,
			'productid': productid,
			'colors': colors,
		}
		data = {'rendered_table': render_to_string('product/color_list.html', context=context)}
		return JsonResponse(data)
	return JsonResponse(data)


def category_products_pro_code(request, id, title):
	category = Category.objects.all()
	products = Product.objects.filter(pro_code = title)
	current_user = request.user
	shopcart = ShopCart.objects.filter(user_id=current_user.id)
	product = Product.objects.all()
	total = 0
	for rs in shopcart:
		total += rs.variant.price * rs.quantity
	quantity = 0
	for rs in shopcart:
		quantity += rs.quantity
	filter_product_title = title
	print(filter_product_title)
	print(type(filter_product_title))
	context = {
		'category':category,
		'products': products,
		'total': total,
		'quantity': quantity,
		'product': product,
		'filter_product_title': filter_product_title
	}
	return render(request, 'product/category_products_pro_code.html',context)


def ajax_manufacturer_allproduct(request):
	data = {}
	if request.POST.get('action') == 'post':
		print(1)
		AllProduct = request.POST.get('AllProduct')
		print(AllProduct)
		products = Product.objects.all()
		# # alltotal = request.POST.get('alltotal')                      
		total2 = request.POST.get('totalID')   
		print(total2)                           
		# # total4 = request.POST.get('total4')                            
		# # total7 = request.POST.get('total7')                             
		# # total13 = request.POST.get('total13')                              
		# # big13 = request.POST.get('big13')
		# # total = request.POST.get('total')
		# # print(total)
		# totalID = request.POST.get('totalID')
		# if totalID == "alltotal":
		# 	print(1)
		# elif totalID == "2000000":
		# 	print(2)
		# elif totalID == 4000000:
		# 	print(4)
		# #print(alltotal, total2, total4, total7, total13, big13)
		# #print(products[1])
		# product = []
		# for i in range(len(products)):
		# 	product.append(products[i])
		# print(product)
		context = {
			'products': products,
		}
		data = {'rendered_table': render_to_string('product/advanced-searchs.html', context=context)}
		return JsonResponse(data)
	return JsonResponse(data)


def ajax_manufacturer_apple(request):
	data = {}
	if request.POST.get('action') == 'post':
		print(1)
		Apple = request.POST.get('Apple')
		print(Apple)
		products = Product.objects.filter(pro_code = Apple)	
		context = {
			'products': products,
		}
		data = {'rendered_table': render_to_string('product/advanced-searchs.html', context=context)}
		return JsonResponse(data)
	return JsonResponse(data)


def ajax_manufacturer_samsung(request):
	data = {}
	if request.POST.get('action') == 'post':
		print(1)
		Samsung = request.POST.get('Samsung')	
		products = Product.objects.filter(pro_code = Samsung)	
		context = {
			'products': products,
		}
		data = {'rendered_table': render_to_string('product/advanced-searchs.html', context=context)}
		return JsonResponse(data)
	return JsonResponse(data)


def ajax_manufacturer_oppo(request):
	data = {}
	if request.POST.get('action') == 'post':
		print(1)
		Oppo = request.POST.get('Oppo')		
		products = Product.objects.filter(pro_code = Oppo)
		context = {
			'products': products,
		}
		data = {'rendered_table': render_to_string('product/advanced-searchs.html', context=context)}
		return JsonResponse(data)
	return JsonResponse(data)


def ajax_manufacturer_vivo(request):
	data = {}
	if request.POST.get('action') == 'post':
		print(1)
		Vivo = request.POST.get('Vivo')		
		products = Product.objects.filter(pro_code = Vivo)
		context = {
			'products': products,
		}
		data = {'rendered_table': render_to_string('product/advanced-searchs.html', context=context)}
		return JsonResponse(data)
	return JsonResponse(data)


def ajax_manufacturer_vsmart(request):
	data = {}
	if request.POST.get('action') == 'post':
		print(1)
		Vsmart = request.POST.get('Vsmart')		
		products = Product.objects.filter(pro_code = Vsmart)
		context = {
			'products': products,
		}
		data = {'rendered_table': render_to_string('product/advanced-searchs.html', context=context)}
		return JsonResponse(data)
	return JsonResponse(data)


def ajax_manufacturer_xiaomi(request):
	data = {}
	if request.POST.get('action') == 'post':
		print(1)
		Xiaomi = request.POST.get('Xiaomi')		
		products = Product.objects.filter(pro_code = Xiaomi)
		context = {
			'products': products,
		}
		data = {'rendered_table': render_to_string('product/advanced-searchs.html', context=context)}
		return JsonResponse(data)
	return JsonResponse(data)


def ajax_manufacturer_realme(request):
	data = {}
	if request.POST.get('action') == 'post':
		print(1)
		Realme = request.POST.get('Realme')
		products = Product.objects.filter(pro_code = Realme)
		context = {
			'products': products,
		}
		data = {'rendered_table': render_to_string('product/advanced-searchs.html', context=context)}
		return JsonResponse(data)
	return JsonResponse(data)


def ajax_manufacturer_masstel(request):
	data = {}
	if request.POST.get('action') == 'post':
		print(1)
		Masstel = request.POST.get('Masstel')		
		products = Product.objects.filter(pro_code = Masstel)
		context = {
			'products': products,
		}
		data = {'rendered_table': render_to_string('product/advanced-searchs.html', context=context)}
		return JsonResponse(data)
	return JsonResponse(data)


def ajax_manufacturer_huawei(request):
	data = {}
	if request.POST.get('action') == 'post':
		print(1)
		Huawei = request.POST.get('Huawei')	
		products = Product.objects.filter(pro_code = Huawei)
		context = {
			'products': products,
		}
		data = {'rendered_table': render_to_string('product/advanced-searchs.html', context=context)}
		return JsonResponse(data)
	return JsonResponse(data)


def ajax_manufacturer_nokia(request):
	data = {}
	if request.POST.get('action') == 'post':
		print(1)
		Nokia = request.POST.get('Nokia')		
		products = Product.objects.filter(pro_code = Nokia)
		context = {
			'products': products,
		}
		data = {'rendered_table': render_to_string('product/advanced-searchs.html', context=context)}
		return JsonResponse(data)
	return JsonResponse(data)


def ajax_manufacturer_totalall(request):
	data = {}
	if request.POST.get('action') == 'post':
		print(1)
		AllProduct = request.POST.get('AllProduct')
		Apple = request.POST.get('Apple')
		Samsung = request.POST.get('Samsung')
		Oppo = request.POST.get('Oppo')
		Vivo = request.POST.get('Vivo')
		Vsmart = request.POST.get('Vsmart')
		Xiaomi = request.POST.get('Xiaomi')
		Realme = request.POST.get('Realme')
		Masstel = request.POST.get('Masstel')
		Huawei = request.POST.get('Huawei')
		Nokia = request.POST.get('Nokia')
		totalall = request.POST.get('totalall')
		print(AllProduct, Apple,Samsung, Oppo, Vivo, Vsmart, Xiaomi, Realme, Masstel, Huawei, Nokia)
		print(totalall)
		context = {
		}
		data = {'rendered_table': render_to_string('product/advanced-searchs.html', context=context)}
		return JsonResponse(data)
	return JsonResponse(data)


def ajax_manufacturer_total2(request):
	data = {}
	if request.POST.get('action') == 'post':
		print(1)
		AllProduct = request.POST.get('AllProduct')
		Apple = request.POST.get('Apple')
		Samsung = request.POST.get('Samsung')
		Oppo = request.POST.get('Oppo')
		Vivo = request.POST.get('Vivo')
		Vsmart = request.POST.get('Vsmart')
		Xiaomi = request.POST.get('Xiaomi')
		Realme = request.POST.get('Realme')
		Masstel = request.POST.get('Masstel')
		Huawei = request.POST.get('Huawei')
		Nokia = request.POST.get('Nokia')
		total2 = request.POST.get('total2')
		print(AllProduct, Apple,Samsung, Oppo, Vivo, Vsmart, Xiaomi, Realme, Masstel, Huawei, Nokia)
		print(total2)
		context = {
		}
		data = {'rendered_table': render_to_string('product/advanced-searchs.html', context=context)}
		return JsonResponse(data)
	return JsonResponse(data)


