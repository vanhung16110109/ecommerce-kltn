from django.shortcuts import render
from apps.product.models import Category, Product, Images, CommentForm, Comment
from django.http.response import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from apps.order.models import ShopCart


# Create your views here.
def product_detail(request):
    return render(request, 'product_detail.html', {})


def category_products(request, id, slug):
    category = Category.objects.all()
    products = Product.objects.filter(category_id = id)
    context = {
        'category':category,
        'products': products,
    }
    return render(request, './category_products.html',context)


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
	context = {
        'comments': comments,
        'product': product,
        'category': category,
        'images': images,
		'total': total,
        'quantity': quantity,
    }
	return render(request, './product_detail.html', context)