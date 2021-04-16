from django.conf import settings
from django.conf.urls.static import static
from datetime import datetime
from django.urls import path, include
from django.contrib import admin



urlpatterns = [
	path('account/', include('apps.account.urls'), name='account'),
    path('chatbot/', include('apps.chatbot.urls'), name='chatbot'),
    path('checkout/', include('apps.checkout.urls'), name='checkout'),
    path('order/', include('apps.order.urls'), name='order'),
    path('product/', include('apps.product.urls'), name='product'),
    path('', include('apps.home.urls'), name='home_page'),
	# path('home/', include('apps.home.urls'), name='home'),
    path('vnlocation/', include('apps.vnlocation.urls'), name='vnlocation'),
	path('admin/', admin.site.urls),
	path('ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



