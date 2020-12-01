from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    path('', views.home),
    path('searched/', views.searched),
    path('popular/', views.popular, name='popular'),
]