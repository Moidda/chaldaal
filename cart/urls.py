from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    path('', views.index),
    path('ajax/add_item/', views.add_item, name='add_item'),
    path('increase_item/<int:product_id>/', views.increase_item),
    path('decrease_item/<int:product_id>/', views.decrease_item),
    path('erase_item/<int:product_id>/', views.erase_item),
]