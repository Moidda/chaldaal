"""chaldaal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('', include('register.urls')),
    path('manage_product/', include('kumpir.urls')),
    path('cart/', include('cart.urls')),
    path('profile/', include('customerProfile.urls')),
    path('rate/', include('productRating.urls')),
    path('checkout/', include('checkout.urls')),
    path('manage_offers/', include('offers.urls')),
    path('history/', include('customerHistory.urls')),
    path('adminProduct/', include('adminProduct.urls')),
    path('bundle-offer/', include('bundleOffer.urls')),
]
