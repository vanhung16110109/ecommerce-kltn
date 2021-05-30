from django.contrib import admin

# Register your models here.
from .models import ShopCart, Order, OrderProduct

class ShopCartAdmin(admin.ModelAdmin):
    # list_display = ['product', 'user','quantity', 'price', 'amount', 'varamount', 'size', 'color']
    list_display = ['product', 'user','quantity', 'price', 'varamount', 'size', 'color']
    list_filter = ['user']


class OrderProductLine(admin.TabularInline):
	model = OrderProduct
	readonly_fields = ('user', 'product', 'price', 'quantity', 'amount')
	can_delete = False
	extra = 0


class OrderAdmin(admin.ModelAdmin):
	list_display = ['first_name', 'last_name', 'phone', 'total', 'status']
	list_filter = ['status']
	readonly_fields	= ('user','first_name', 'last_name', 'address', 'phone',  'ip', 'total' )
	can_delete = False
	inlines = [OrderProductLine]


class OrderProductAdmin(admin.ModelAdmin):
	list_display = ['user', 'product', 'price', 'quantity', 'amount']
	list_filter = ['user']
	


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(ShopCart, ShopCartAdmin)
