from django.conf import settings
from django.conf.urls.static import static
from datetime import datetime
from django.urls import path, include
from django.contrib import admin
from apps.product.views import ajaxcolor
from django.conf.urls import url
import apps.vnpay_python.views

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

    path('vnpay/', apps.vnpay_python.views.index, name='index'),
    path('vnpay/payment', apps.vnpay_python.views.payment, name='payment'),
    path('vnpay/payment_ipn', apps.vnpay_python.views.payment_ipn, name='payment_ipn'),
    path('vnpay/payment_return', apps.vnpay_python.views.payment_return, name='payment_return'),
    path('vnpay/query', apps.vnpay_python.views.query, name='query'),
    path('vnpay/refund', apps.vnpay_python.views.refund, name='refund'),
    # url(r'^$', apps.vnpay_python.views.index, name='index'),
    # url(r'^payment$', apps.vnpay_python.views.payment, name='payment'),
    # url(r'^payment_ipn$', apps.vnpay_python.views.payment_ipn, name='payment_ipn'),
    # url(r'^payment_return$', apps.vnpay_python.views.payment_return, name='payment_return'),
    # url(r'^query$', apps.vnpay_python.views.query, name='query'),
    # url(r'^refund$', apps.vnpay_python.views.refund, name='refund'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
