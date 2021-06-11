from django.urls import path, include
from apps.account.views import account_login, account_register, account_logout, account_information_view, account_information_update, account_password_update, user_orders, user_order_product_detail
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', account_login, name='login'),
    #path('login/', auth_views.LoginView.as_view(), name='account_login'),
	path('register/', account_register, name='account_register'),
    path('logout/', account_logout, name='account_logout'),
    path('information/', account_information_view, name='account_information_view'),
    path('information-update/', account_information_update, name='account_information_update'),
    path('changepassword/', account_password_update, name='account_password_update'),

	#reset password
	path('reset_password/', auth_views.PasswordResetView.as_view(template_name='account/password_reset.html'), name='reset_password'),
	path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_sent.html'), name='password_reset_done'),
	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html'), name='password_reset_confirm'),
	path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_done.html'), name='password_reset_complete'),

	#user_list_orders
	path('user_orders', user_orders, name='user_orders'),
	path('user_orders_product/<int:id>', user_order_product_detail, name='user_order_product_detail'),
	# path('order_product_detail/<int:id>/<int:oid>', user_order_product_detail, name='user_order_product_detail'),
    
]