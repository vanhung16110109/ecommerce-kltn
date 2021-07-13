from django.urls import path
from apps.product.views import category_products, product_detail, addcomment, CompareProduct

urlpatterns = [
    path('category/<int:id>/<slug:slug>', category_products, name='category_products'),
    path('<int:id>/<slug:slug>', product_detail, name='products_detail'),
    path('addcomment/<int:id>', addcomment, name='addcomment'),
    path('compare/', CompareProduct, name='compare'),
    
]
