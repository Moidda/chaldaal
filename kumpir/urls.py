from django.urls import path
from . import views

urlpatterns = [
    path('manage_product/', views.manage_product),
    path('insert_product/', views.insert_product),
]