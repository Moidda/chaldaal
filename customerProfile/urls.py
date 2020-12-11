from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    path('', views.customer_profile, name="customer_profile"),
    path('save_changes/', views.save_changes, name="save_changes"),
    path('customer-list/', views.customer_list, name="customer-list"),
]