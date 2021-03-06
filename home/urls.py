from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    path('', views.home, name='home'),
    path('popular/', views.popular, name='popular'),
    path('searched/', views.searched, name='searched'),
    path('show_product_search/<slug:searched_item>/', views.show_product_search, name='show_product_search'),
    path('show_product_category/<slug:category>/', views.show_product_category, name='show_product_category'),
    path('show_product_flash_sale/', views.show_product_flash_sale, name='show_product_flash_sale'),
    path('show_bundle_offer/', views.show_bundle_offer, name='show_bundle_offer'),
    path('sub_category/<slug:sub_category>/', views.show_sub_category, name='show_sub_category'),
    path('ajax/get_subcategory_filter/', views.get_subcategory_filter, name='get_subcategory_filter'),
    path('ajax/flash-sale-count/', views.flash_sale_count, name='flash-sale-count'),
    path('covid_19_protection/', views.covid, name='covid'),
]