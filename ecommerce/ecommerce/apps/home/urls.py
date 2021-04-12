from django.urls import path
from apps.home.views import home_page

urlpatterns = [
	path('', home_page, name='home_page'),
	# path('contact/', contact, name='contact'),
    # path('about/', about_us, name='about'),
]