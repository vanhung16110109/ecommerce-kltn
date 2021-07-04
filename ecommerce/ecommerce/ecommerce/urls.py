from django.conf import settings
from django.conf.urls.static import static
from datetime import datetime
from django.urls import path, include
from django.contrib import admin
from apps.product.views import ajaxcolor
from apps.vnlocation.views import ajaxAPIlocationdistrict, ajaxAPIlocationward, ajaxGHTK, ajaxGHN, ajaxGHN_online, ajaxGHTK_online
from django.conf.urls import url
import apps.vnpay_python.views
from apps.product.views import category_products_pro_code


urlpatterns = [
	path('account/', include('apps.account.urls'), name='account'),
    path('chatbot/', include('apps.chatbot.urls'), name='chatbot'),
    path('checkout/', include('apps.checkout.urls'), name='checkout'),
    path('order/', include('apps.order.urls'), name='order'),
    path('product/', include('apps.product.urls'), name='product'),
    path('', include('apps.home.urls'), name='home'),
	path('social-auth/', include('social_django.urls', namespace='social')),
	#path('oauth/', include('social_django.urls', namespace='social')),  # <-- here
    path('vnlocation/', include('apps.vnlocation.urls'), name='vnlocation'),
	path('admin/', admin.site.urls),
	path('ckeditor/', include('ckeditor_uploader.urls')),
	path('ajaxcolor/', ajaxcolor, name='ajaxcolor'),
    path('ajaxAPIlocationdistrict/', ajaxAPIlocationdistrict, name='ajaxAPIlocationdistrict'),
    path('ajaxAPIlocationward/', ajaxAPIlocationward, name='ajaxAPIlocationward'),
    path('ajaxGHTK/', ajaxGHTK, name='ajaxGHTK'),
    path('ajaxGHN/', ajaxGHN, name='ajaxGHN'),
    path('ajaxGHTK_online/', ajaxGHTK_online, name='ajaxGHTK_online'),
    path('ajaxGHN_online/', ajaxGHN_online, name='ajaxGHN_online'),
    path('category/<int:id>/<slug:title>', category_products_pro_code, name='category_products_pro_code'),

	path('payment/', include('apps.vnpay_python.urls'), name='payment'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
