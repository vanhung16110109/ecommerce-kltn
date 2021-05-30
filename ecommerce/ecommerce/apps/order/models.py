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
		('Mới', 'Mới'),
		('Chuẩn bị', 'Chuẩn bị'),
		('Đang giao hàng', 'Đang giao hàng'),
		('Hoàn thành', 'Hoàn thành'),
		('Đã hủy', 'Đã hủy')
	)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	code = models.CharField(max_length=5, editable=False)
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	phone = models.CharField(blank=True, max_length=20)
	address = models.CharField(blank=True, max_length=255)
	# city = models.CharField(blank=True, max_length=50)
	# country = models.CharField(blank=True, max_length=50)
	total = models.FloatField()
	status = models.CharField(max_length=50, choices=STATUS,default='Mới')
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




