from django.urls import path
from . import views


urlpatterns = [
    path('<int:isCustomer>/', views.history, name='history'),
]