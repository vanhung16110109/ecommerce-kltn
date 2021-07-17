from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import authenticate, get_user_model, login, logout, update_session_auth_hash
from django.contrib import messages
from apps.account.models import UserProfile
# Create your views here.
from django.http.response import HttpResponseRedirect
from apps.account.forms import RegisterForm, LoginForm, ProfileUpdateForm
from apps.product.models import Category
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from apps.order.models import ShopCart, Order, OrderProduct
from apps.product.models import Category, Product, Images, CommentForm, Comment, Variants, ProductAdvancedSearch, Compare


# login
def account_login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			current_user = request.user
			user_id = current_user.id
			print(user_id)
			userprofile = UserProfile.objects.get(user_id = current_user.id)
			request.session['userimage'] = userprofile.image.url
			check = 1
			return HttpResponseRedirect('/')
		else:
			check = 0
			return render(request,'account/login.html', {'check': check})
			return HttpResponseRedirect('/account/login')

	return render(request, 'account/login.html',{})


#register
def account_register(request):
	form = RegisterForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password')
		email = form.cleaned_data.get('email')
		new_user = User.objects.create_user(username,email,password)
		new_user.is_staff = True        # set staff
		new_user.save()
		print(new_user)
		user = authenticate(username=username, password=password)
		login(request, user)
		#create data profile
		current_user = request.user
		data_userprofile = UserProfile()
		data_userprofile.user_id = current_user.id
		data_userprofile.image = "user.png"
		data_userprofile.save()
		userprofile = UserProfile.objects.get(user_id = current_user.id)
		request.session['userimage'] = userprofile.image.url
		check = 1
		return render(request,'account/register.html', {'check': check})
		return HttpResponseRedirect('/')

	return render(request, 'account/register.html', {})


#logout
def account_logout(request):
	logout(request)
	print('logout success')
	return HttpResponseRedirect('/')


#view information
@login_required(login_url='/account/login')
def account_information_view(request):
	category = Category.objects.all()
	current_user = request.user
	user_id = current_user.id

	profile = UserProfile.objects.get(user_id = current_user.id)
	current_user = request.user
	image_default = "user.png"
	shopcart = ShopCart.objects.filter(user_id=current_user.id)
	#print(current_user.email)
	email_user = current_user.email
	total = 0
	for rs in shopcart:
		total += rs.variant.price * rs.quantity
	quantity = 0
	for rs in shopcart:
		quantity += rs.quantity
	context={
		'category':category,
		'profile': profile,
		'total': total,
		'quantity': quantity,
		'email_user': email_user
	}
	return render(request, 'account/information.html', context)


#change information
@login_required(login_url='/account/login')
def account_information_update(request):
	if request.method == 'POST':
		profile_form = ProfileUpdateForm(request.POST,request.FILES, instance=request.user.userprofile)
		if profile_form.is_valid():
			profile_form.save()
			messages.success(request, 'Thay đổi thông tin thành công')
			current_user = request.user
			userprofile = UserProfile.objects.get(user_id = current_user.id)
			request.session['userimage'] = userprofile.image.url
			shopcart = ShopCart.objects.filter(user_id=current_user.id)
			return redirect('/account/information/')
	else:
		profile_form = ProfileUpdateForm(instance=request.user.userprofile)
		current_user = request.user
		user_id = current_user.id
		print(user_id)
		shopcart = ShopCart.objects.filter(user_id=current_user.id)
		total = 0
		for rs in shopcart:
			total += rs.variant.price * rs.quantity
		quantity = 0
		for rs in shopcart:
			quantity += rs.quantity
		context = {
			'profile_form': profile_form,
			'total': total,
			'quantity': quantity,
		}
	return render(request, 'account/information_update.html', context)


#change password
@login_required(login_url='/account/login')
def account_password_update(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)
			messages.success(request,'Thay đổi mật khẩu thành công')
			return HttpResponseRedirect('/account/information/')
		else:
			messages.error(request, 'Thay đổi mật khẩu không thành công, xin vui lòng kiểm tra lại')
			return HttpResponseRedirect('/account/changepassword/')
	else:
		category = Category.objects.all()
		form = PasswordChangeForm(request.user)
		current_user = request.user
		user_id = current_user.id
		print(user_id)
		shopcart = ShopCart.objects.filter(user_id=current_user.id)
		total = 0
		for rs in shopcart:
			total += rs.variant.price * rs.quantity
		quantity = 0
		for rs in shopcart:
			quantity += rs.quantity
		context = {
			'category': category,
			'form':form,
			'total': total,
			'quantity': quantity,
		}
	return render(request, 'account/changepassword.html', context)



@login_required(login_url='/account/login')
def user_orders(request):
	category = Category.objects.all()
	current_user = request.user
	user_id = current_user.id
	order_product = OrderProduct.objects.filter(user_id=current_user.id).order_by('-id')
	shopcart = ShopCart.objects.filter(user_id=current_user.id)
	orders = Order.objects.filter(user_id=current_user.id)
	total = 0
	for rs in shopcart:
		total += rs.variant.price * rs.quantity
	quantity = 0
	for rs in shopcart:
		quantity += rs.quantity
	context={
		'category':category,
		'total': total,
		'quantity': quantity,
		'orders': orders,
		'order_product': order_product,
	}
	return render(request, 'account/user_orders.html', context)



@login_required(login_url='/account/login')
def user_order_product_detail(request,id):
	current_user = request.user
	order = Order.objects.get(user_id=current_user.id, id=id)
	orderitems = OrderProduct.objects.filter(order_id=id)
	category = Category.objects.all()
	shopcart = ShopCart.objects.filter(user_id=current_user.id)
	orders = Order.objects.filter(user_id=current_user.id)
	order_product = OrderProduct.objects.filter(user_id=current_user.id).order_by('-id')
	total = 0
	for rs in shopcart:
		total += rs.variant.price * rs.quantity
	quantity = 0
	for rs in shopcart:
		quantity += rs.quantity
	context = {
		'category': category,
		'order': order,
		'orders': orders,
		'orderitems': orderitems,
		'category':category,
		'total': total,
		'quantity': quantity,
		'order_product': order_product,
	}
	return render(request, 'account/user_order_detail.html', context)


@login_required(login_url='/account/login')
def user_comments(request):
	#category = Category.objects.all()
	current_user = request.user
	comments = Comment.objects.filter(user_id=current_user.id)
	context = {
		#'category': category,
		'comments': comments,
	}
	return render(request, 'user_comments.html', context)


# @login_required(login_url='/account/login')
# def user_order_product(request):
#     #category = Category.objects.all()
#     current_user = request.user
#     order_product = OrderProduct.objects.filter(user_id=current_user.id).order_by('-id')
#     context = {#'category': category,
#                'order_product': order_product,
#                }
#     return render(request, 'user_order_products.html', context)

@login_required(login_url='/account/login')
def user_deletecomment(request,id):
	current_user = request.user
	Comment.objects.filter(id=id, user_id=current_user.id).delete()
	messages.success(request, 'Comment deleted..')
	return HttpResponseRedirect('/user/comments')

