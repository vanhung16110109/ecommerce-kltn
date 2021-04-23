from django.urls import path
from .views import addtoshopcart, deletefromcart, orderproduct, shopcart



urlpatterns = [
	path('', shopcart),
    path('addtoshopcart/<int:id>', addtoshopcart, name='addtoshopcart'),
    path('deletefromcart/<int:id>', deletefromcart, name='deletefromcart'),
	path('orderproduct/', orderproduct, name='orderproduct'),
]