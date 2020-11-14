from django.urls import path
from . import views

urlpatterns = [
    path('sign_up/', views.sign_up),
    path('log_in/', views.log_in),
    path('log_in_verification/', views.log_in_verification),
    path('sign_up_verification/', views.sign_up_verification),
]