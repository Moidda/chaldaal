from django.urls import path
from . import views

urlpatterns = [
    path('', views.manage_product),
    path('insert_product/', views.insert_product),
    path('stock/', views.stock),
    path('stock/change_stock/', views.change_stock),
]