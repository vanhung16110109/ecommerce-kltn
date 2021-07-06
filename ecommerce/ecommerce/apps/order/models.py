from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from apps.product.models import Product, Variants
from django.forms import ModelForm
from django.forms.widgets import FileInput, Select, TextInput


class ShopCart(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	variant = models.ForeignKey(Variants, on_delete=models.SET_NULL,blank=True, null=True)
	quantity = models.IntegerField()
	
	def __str__(self):
		return self.product.title

	# @property
	# def price(self):
	#     return (self.product.price)

	@property
	def price(self):
		return (self.variant.price)

	@property
	def amount(self):
		return (self.quantity * self.product.price)   

	@property
	def varamount(self):
		return (self.quantity * self.variant.price)

	@property
	def size(self):
		return self.variant.size

	@property
	def color(self):
		return self.variant.color


class ShopCartForm(ModelForm):
	class Meta:
		model = ShopCart
		fields = ['quantity']


class Order(models.Model):
	STATUS = (
		('Đang chờ xác nhận', 'Đang chờ xác nhận'),
		('Chuẩn bị giao hàng', 'Chuẩn bị giao hàng'),
		('Đang giao hàng', 'Đang giao hàng'),
		('Hoàn thành', 'Hoàn thành'),
		('Đã hủy', 'Đã hủy')
	)
	STATUS_PAY = (
		('Chưa thanh toán', 'Chưa thanh toán'),
		('Đã thanh toán', 'Đã thanh toán')
	)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	code = models.CharField(max_length=5, editable=False)
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	phone = models.CharField(blank=True, max_length=20)
	province = models.CharField(blank=True, max_length=255)
	district = models.CharField(blank=True, max_length=255)
	ward = models.CharField(blank=True, max_length=255)
	address = models.CharField(blank=True, max_length=255)
	# city = models.CharField(blank=True, max_length=50)
	# country = models.CharField(blank=True, max_length=50)
	total = models.IntegerField()
	status = models.CharField(max_length=50, choices=STATUS,default='Đang chờ xác nhận')
	status_pay = models.CharField(max_length=50, choices=STATUS_PAY,default='Chưa thanh toán')
	delivery = models.CharField(blank=True, max_length=255)
	transport_fee =  models.IntegerField()
	ip = models.CharField(blank=True, max_length=30)
	adminnote = models.CharField(blank=True, max_length=50)
	create_at =  models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.user.first_name
	

class OrderForm(ModelForm):
	class Meta:
		model = Order
		fields = ['first_name','last_name','address','phone']

		# fields = ['first_name','last_name','address','phone','city','country']

class OrderProduct(models.Model):
	STATUS = (
		('Mới', 'Mới'),
		('Đã được chấp nhận', 'Đã được chấp nhận'),
		('Đã hủy', 'Đã hủy'),
	)
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	variant = models.ForeignKey(Variants, on_delete=models.SET_NULL,blank=True, null=True)
	quantity = models.IntegerField()
	price = models.FloatField()
	amount = models.FloatField()
	status = models.CharField(max_length=50, choices=STATUS, default='Mới')
	create_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.product.title



class OrderWaitingPayment(models.Model):
	STATUS = (
		('Đang chờ xác nhận', 'Đang chờ xác nhận'),
		('Chuẩn bị giao hàng', 'Chuẩn bị giao hàng'),
		('Đang giao hàng', 'Đang giao hàng'),
		('Hoàn thành', 'Hoàn thành'),
		('Đã hủy', 'Đã hủy')
	)
	STATUS_PAY = (
		('Chưa thanh toán', 'Chưa thanh toán'),
		('Đã thanh toán', 'Đã thanh toán')
	)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	code = models.CharField(max_length=5, editable=False)
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	phone = models.CharField(blank=True, max_length=20)
	province = models.CharField(blank=True, max_length=255)
	district = models.CharField(blank=True, max_length=255)
	ward = models.CharField(blank=True, max_length=255)
	address = models.CharField(blank=True, max_length=255)
	total = models.IntegerField()
	status = models.CharField(max_length=50, choices=STATUS,default='Đang chờ xác nhận')
	status_pay = models.CharField(max_length=50, choices=STATUS_PAY,default='Chưa thanh toán')
	delivery = models.CharField(blank=True, max_length=255)
	transport_fee =  models.IntegerField()
	ip = models.CharField(blank=True, max_length=30)
	adminnote = models.CharField(blank=True, max_length=50)
	create_at =  models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.user.first_name