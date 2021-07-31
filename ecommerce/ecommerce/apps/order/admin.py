from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# Register your models here.
from .models import ShopCart, Order, OrderProduct, OrderWaitingPayment

class ShopCartAdmin(admin.ModelAdmin):
    # list_display = ['product', 'user','quantity', 'price', 'amount', 'varamount', 'size', 'color']
    list_display = ['product', 'user','quantity', 'price', 'varamount', 'size', 'color']
    list_filter = ['user']


class OrderProductLine(admin.TabularInline):
	model = OrderProduct
	readonly_fields = ('user', 'product', 'price', 'quantity', 'amount')
	can_delete = False
	extra = 0


class OrderAdmin(ImportExportModelAdmin):
	list_display = ['first_name', 'last_name', 'phone', 'total', 'status', 'status_pay']
	list_filter = ['status', 'status_pay', 'delivery']
	readonly_fields	= ('user','first_name', 'last_name','province','district', 'ward', 'address', 'phone', 'delivery', 'transport_fee', 'ip', 'total', 'code')
	can_delete = False
	inlines = [OrderProductLine]


class OrderProductAdmin(admin.ModelAdmin):
	list_display = ['user', 'product', 'price', 'quantity', 'amount']
	list_filter = ['user']
	

class OrderWaitingPaymentAdmin(admin.ModelAdmin):
	list_display = ['first_name', 'last_name', 'phone', 'total', 'status']
	list_filter = ['status', 'status_pay']
	readonly_fields	= ('user','first_name', 'last_name','province','district', 'ward', 'address', 'phone', 'delivery', 'transport_fee', 'ip', 'total', 'code')
	can_delete = False


admin.site.register(Order, OrderAdmin)
#admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(ShopCart, ShopCartAdmin)
#admin.site.register(OrderWaitingPayment, OrderWaitingPaymentAdmin)
