from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    path('', views.checkout, name='checkout'), # /checkout/
    path('confirm_checkout/', views.confirm_checkout, name='confirm_checkout'), # /checkout/confirm_checkout
    path('using_points/', views.using_points, name='using_points'), # checkout/using_points
]