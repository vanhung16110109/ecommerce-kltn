from django.db.models import query
from django.shortcuts import render
from apps.product.models import Category, Product, Images, CommentForm, Comment, Variants, ProductAdvancedSearch, Compare
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
    comments = Comment.objects.filter(product_id=id,status='True')
    product_list = Compare.objects.all()
    compare_result = Compare.objects.get(product=product)
    context = {
        'comments': comments,
        'product': product,
        'category': category,
        'images': images,
        'total': total,
        'quantity': quantity,
        # 'deta': details,
        'compare_result': compare_result,
        'product_list': product_list,
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
        #print(size_id)
        #print(productid)
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
    #print(filter_product_title)
    #print(type(filter_product_title))
    context = {
        'category':category,
        'products': products,
        'total': total,
        'quantity': quantity,
        'product': product,
        'filter_product_title': filter_product_title
    }
    return render(request, 'product/category_products_pro_code.html',context)


def my_product(i):
    return i[0].price


def ajax_manufacturer(request):
    data = {}
    if request.POST.get('action') == 'post':
        productName = request.POST.get('_productName')
        typeNamePrice = request.POST.get('_typeNamePrice')
        typeNameCamera = request.POST.get('_typeNameCamera')
        typeNamePin = request.POST.get('_typeNamePin')
        typeNameSortProduct = request.POST.get('_typeNameSortProduct')
        #print(productName, typeNamePrice, typeNameCamera, typeNamePin, typeNameSortProduct)

          # products = Product.objects.all()
        # products_result = []
        temp_products_result = []
        #loại điện thoại
        if productName == 'AllProduct':
            products_result = Product.objects.all()
        else:
            products_result = Product.objects.filter(pro_code = productName)

        # giá điện thoại
        if typeNamePrice == 'totalID1':	# tất cả
            if productName == 'AllProduct':
                products_result = Product.objects.all()
            else:
                products_result = Product.objects.filter(pro_code = productName)
        elif typeNamePrice == 'totalID2': # 0 - 2000000
            for rs in products_result:
                price = int((rs.price)*1000000)
                if  price > 0 and price <= 2000000:
                    temp_products_result.append(rs)
            products_result = temp_products_result
            temp_products_result = []
        elif typeNamePrice == 'totalID3': # 2000000 - 4000000
            for rs in products_result:
                price = int((rs.price)*1000000)
                if  price >= 2000000 and price <= 4000000:
                    temp_products_result.append(rs)
            products_result = temp_products_result
            temp_products_result = []
        elif typeNamePrice == 'totalID4': # 4000000 - 7000000
            for rs in products_result:
                price = int((rs.price)*1000000)
                if  price >= 4000000 and price <= 7000000:
                    temp_products_result.append(rs)
            products_result = temp_products_result
            temp_products_result = []
        elif typeNamePrice == 'totalID5': # 7000000 - 13000000
            for rs in products_result:
                price = int((rs.price)*1000000)
                if  price >= 7000000 and price <= 13000000:
                    temp_products_result.append(rs)
            products_result = temp_products_result
            temp_products_result = []
        elif typeNamePrice == 'totalID6': # lớn hơn 13000000
            for rs in products_result:
                price = int((rs.price)*1000000)
                if  price > 13000000:
                    temp_products_result.append(rs)
            products_result = temp_products_result
            temp_products_result = []
        #print(products_result)
        # hoàn thành lấy price
        # filter camera
        productAdvancedSearch = ProductAdvancedSearch.objects.all()
        temp_products_result_camera = []
        if typeNameCamera == 'cameraID1':	#tất cả
            products_result
        elif typeNameCamera == 'cameraID2':	#Quay phim slow motion
            for rs in productAdvancedSearch:
                if rs.camera_slow_motion == 'Có':
                    temp_products_result_camera.append(rs.product)
            # có temp
            for rs in products_result:
                for rs_camera in temp_products_result_camera:
                    if rs == rs_camera:
                        temp_products_result.append(rs)
            products_result = temp_products_result
            temp_products_result_camera = []
            temp_products_result = []
        elif typeNameCamera == 'cameraID3':			# AI
            for rs in productAdvancedSearch:
                if rs.camera_ai == 'Có':
                    temp_products_result_camera.append(rs.product)
            # có temp
            for rs in products_result:
                for rs_camera in temp_products_result_camera:
                    if rs == rs_camera:
                        temp_products_result.append(rs)
            products_result = temp_products_result
            temp_products_result_camera = []
            temp_products_result = []
        elif typeNameCamera == 'cameraID4':			# 3d
            for rs in productAdvancedSearch:
                if rs.camera_3d == 'Có':
                    temp_products_result_camera.append(rs.product)
            # có temp
            for rs in products_result:
                for rs_camera in temp_products_result_camera:
                    if rs == rs_camera:
                        temp_products_result.append(rs)
            products_result = temp_products_result
            temp_products_result_camera = []
            temp_products_result = []
        elif typeNameCamera == 'cameraID5':	#Hiệu ứng làm đẹp
            for rs in productAdvancedSearch:
                if rs.camera_beauty_effect == 'Có':
                    temp_products_result_camera.append(rs.product)
            # có temp
            for rs in products_result:
                for rs_camera in temp_products_result_camera:
                    if rs == rs_camera:
                        temp_products_result.append(rs)
            products_result = temp_products_result
            temp_products_result_camera = []
            temp_products_result = []
        elif typeNameCamera == 'cameraID6':	#Zoom quang học
            for rs in productAdvancedSearch:
                if rs.camera_optical_zoom == 'Có':
                    temp_products_result_camera.append(rs.product)
            # có temp
            for rs in products_result:
                for rs_camera in temp_products_result_camera:
                    if rs == rs_camera:
                        temp_products_result.append(rs)
            products_result = temp_products_result
            temp_products_result_camera = []
            temp_products_result = []
        # đã done camera
        # tính dung lượng pin
        temp_products_result_pin = []
        if typeNamePin == 'PinID1':
            products_result
        elif typeNamePin == 'PinID2':			# dưới 3000
            for rs in productAdvancedSearch:
                if rs.battery_capacity < 3000:
                    temp_products_result_pin.append(rs.product)
            # có temp
            for rs in products_result:
                for rs_pin in temp_products_result_pin:
                    if rs == rs_pin:
                        temp_products_result.append(rs)
            products_result = temp_products_result
            temp_products_result_pin = []
            temp_products_result = []
        elif typeNamePin == 'PinID3':	# 3000 - 4000
            for rs in productAdvancedSearch:
                if rs.battery_capacity >= 3000 and rs.battery_capacity <= 4000:
                    temp_products_result_pin.append(rs.product)
            # có temp
            for rs in products_result:
                for rs_pin in temp_products_result_pin:
                    if rs == rs_pin:
                        temp_products_result.append(rs)
            products_result = temp_products_result
            temp_products_result_pin = []
            temp_products_result = []
        elif typeNamePin == 'PinID4':	# > 4000
            for rs in productAdvancedSearch:
                if rs.battery_capacity > 4000:
                    temp_products_result_pin.append(rs.product)
            # có temp
            for rs in products_result:
                for rs_pin in temp_products_result_pin:
                    if rs == rs_pin:
                        temp_products_result.append(rs)
            products_result = temp_products_result
            temp_products_result_pin = []
            temp_products_result = []

        #sap xep tang giam
        typeNameSortProduct = int(typeNameSortProduct)

        
        
        if typeNameSortProduct == 0:
                products_result
        elif typeNameSortProduct == 1:
            if (products_result) == 1:
                products_result
            elif len(products_result) == 0:
                products_result
            else:
                # if isinstance(products_result, list) == True:
                #     products_result = products_result.sort(key = my_product)
                #     print(products_result)
                products_result = products_result.order_by('-price')
        elif typeNameSortProduct == 2:
            if len(products_result) == 1:
                products_result
            elif len(products_result) == 0:
                products_result 
            else:
                products_result = products_result.order_by('price')
        context = {
            'products_result': products_result,
        }
        data = {'rendered_table': render_to_string('product/advanced-searchs.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)


def CompareProduct(request):
    data = {}
    if request.POST.get('action') == 'post':
        product_list = Compare.objects.all()
        smartphoneName = request.POST.get('SmartphoneName')
        
        product = Product.objects.all()
        # return về id product và slug
        for rs in product:
            if rs.title == smartphoneName:
                product_id = rs.id
                product_slug = rs.slug
        #product_id
        #return chi tiết so sánh
        for rs in product_list:
            if str(rs.product) == smartphoneName:
                compare_result = rs
        
        context = {
            'smartphoneName':smartphoneName,
            'product_list': product_list,
            'compare_result': compare_result,
            'product_id': product_id,
            'product_slug': product_slug
        }
        data = {'rendered_table': render_to_string('product/product-compare.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)
