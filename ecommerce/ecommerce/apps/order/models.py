from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from apps.product.models import Product
from django.forms import ModelForm
from django.forms.widgets import FileInput, Select, TextInput

class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.DecimalField(max_digits=20, decimal_places=0)
    

    def __str__(self):
        return self.product.title

    @property
    def price(self):
        return (self.product.price)

    @property
    def amount(self):
        return (self.quantity * self.product.price)    


class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields = ['quantity']


class Order(models.Model):
	STATUS = (
		('New', 'New'),
		('Preparing', 'Preparing'),
		('OnShipping', 'OnShipping'),
		('Canceled', 'Canceled')
	)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	code = models.CharField(max_length=5, editable=False)
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	phone = models.CharField(blank=True, max_length=20)
	address = models.CharField(blank=True, max_length=255)
	city = models.CharField(blank=True, max_length=50)
	country = models.CharField(blank=True, max_length=50)
	total = models.FloatField()
	status = models.CharField(max_length=10, choices=STATUS,default='New')
	ip = models.CharField(blank=True, max_length=30)
	adminnote = models.CharField(blank=True, max_length=50)
	create_at =  models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.user.first_name
	

class OrderForm(ModelForm):
	class Meta:
		model = Order
		fields = ['first_name','last_name', 'address', 'phone', 'city', 'country']


class OrderProduct(models.Model):
	STATUS = (
		('New', 'New'),
		('Accepted', 'Accepted'),
		('Canceled', 'Canceled')
	)
	order = models.ForeignKey(Order,on_delete=models.CASCADE)
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	product = models.ForeignKey(Product,on_delete=models.CASCADE)
	quantity = models.IntegerField()
	price = models.FloatField()
	amount = models.FloatField()
	status = models.CharField(max_length=10,choices=STATUS,default='New')
	create_at =  models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.product.title



	