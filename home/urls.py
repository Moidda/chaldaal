from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    path('', views.home),
    path('searched/', views.searched),
    path('cart_func/<int:product_id>/', views.cart_func),
]