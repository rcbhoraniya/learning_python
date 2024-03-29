"""coreinv URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views

from django.conf.urls.static import static                      # used for static files

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    # path('', include('homepage.urls')),
    path('', include('inventory.urls')),
    path('authentication/', include('authentication.urls')),
    path('sales/', include('sales.urls')),
    path('purchase/', include('purchase.urls')),
    path('apis-inventory/', include('inventory.apis.urls')),
    path('apis-sales/', include('sales.apis.urls')),
    path('apis-purchase/', include('purchase.apis.urls')),

]