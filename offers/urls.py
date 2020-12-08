from django.urls import path
from . import views

urlpatterns = [
    path('', views.manage_offers, name='manage_offers'),
    path('percent_off/', views.create_flash_sale, name='percent_off'),
    path('sale_list/', views.sale_list),
    path('sale_list/end_sale/<int:flash_sale_id>/', views.end_sale)
]