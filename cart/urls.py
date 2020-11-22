from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    path('', views.index),
    path('add_item/<int:product_id>/', views.add_item),
    path('increase_item/<int:product_id>/', views.increase_item),
    path('decrease_item/<int:product_id>/', views.decrease_item),
    path('erase_item/<int:product_id>/', views.erase_item),
]