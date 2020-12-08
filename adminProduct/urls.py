from django.urls import path
from . import views


urlpatterns = [
    path('<int:product_id>/', views.edit_product, name='edit_product'),
    path('save_changes/<int:product_id>', views.save_changes, name='save_admin_changes'),
]