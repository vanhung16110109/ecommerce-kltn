from django.conf.urls import url
from django.contrib import admin
import apps.vnpay_python.views

urlpatterns = [
    url(r'^$', apps.vnpay_python.views.index, name='index'),
    url(r'^payment$', apps.vnpay_python.views.payment, name='payment'),
    url(r'^payment_ipn$', apps.vnpay_python.views.payment_ipn, name='payment_ipn'),
    url(r'^payment_return$', apps.vnpay_python.views.payment_return, name='payment_return'),
    url(r'^query$', apps.vnpay_python.views.query, name='query'),
    url(r'^refund$', apps.vnpay_python.views.refund, name='refund'),
]
