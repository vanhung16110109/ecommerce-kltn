from django.urls import path
from apps.home.views import home_page
from apps.search.views import search, search_auto

urlpatterns = [
	path('', home_page, name='home'),
	path('search/', search, name='search'),
    path('search_auto/', search_auto, name='search_auto'),
	# path('contact/', contact, name='contact'),
    # path('about/', about_us, name='about'),
]