from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    path('', views.home),
    path('popular/', views.popular, name='popular'),
    path('searched/', views.searched),
    path('show_product_search/<slug:searched_item>/', views.show_product_search, name='show_product_search'),
    path('show_product_category/<slug:category>/', views.show_product_category, name='show_product_category'),
]