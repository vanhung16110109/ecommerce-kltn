from django.urls import path
from .views import order_add,  order_delete, order_detail


urlpatterns = [ 
    path('order_add/<int:id>', order_add, name='order_add'),
    path('order_delete/<int:id>', order_delete, name='order_delete'),
	path('order_detail/', orderproduct, name='order_detail'),
] 