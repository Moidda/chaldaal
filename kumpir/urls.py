from django.urls import path
from . import views

urlpatterns = [
    path('', views.manage_product, name='manage_product'),
    path('insert_product/', views.insert_product),
    path('stock/', views.stock),
    path('stock/change_stock/', views.change_stock, name='change_stock'),
    path('stock/ajax/get_products/', views.get_products, name='get_products'),
    path('ajax/get_stock/', views.get_stock, name='get_stock'),
]