from django.urls import path, include
from apps.vnlocation.views import demo,user_order_product_detail, user_order_product


urlpatterns = [
    path('', demo, name='demo'),
    path('orders_product/', user_order_product, name='user_order_product'),
    path('order_product_detail/<int:id>/<int:oid>', user_order_product_detail, name='user_order_product_detail'),
]