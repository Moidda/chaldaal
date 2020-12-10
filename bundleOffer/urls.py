from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    path('', views.bundleOffer, name='bundle-offer'),
    path('bundle-list/', views.bundle_list, name='bundle-list'),
    path('bundle-end/<int:bundle_id>', views.bundle_end, name='bundle-end'),
    path('ajax/create_bundle_offer/', views.create_bundle_offer, name='create_bundle_offer')
]