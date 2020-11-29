from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    path('', views.rating),
    path('increase_rating/<int:pid>/', views.increase_rating, name='increase_rating'),
    path('decrease_rating/<int:pid>/', views.decrease_rating, name='decrease_rating'),
    path('save_rating/', views.save_rating, name='save_rating'),
]