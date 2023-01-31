from django.urls import path
# from django.conf.urls import url
from django.views.generic.dates import ArchiveIndexView
from .models import *
from . import views
app_name = 'inventory'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about', views.AboutView.as_view(), name='about'),

    path('inventory-list', views.InventoryListView.as_view(), name='inventory-list'),
    path('inventory/new', views.InventoryCreateView.as_view(), name='new-inventory'),
    path('inventory/<pk>/edit', views.InventoryUpdateView.as_view(), name='edit-inventory'),
    path('inventory/<pk>/delete', views.InventoryDeleteView.as_view(), name='delete-inventory'),
    path('inventory/<product>', views.InventoryLogView.as_view(), name='inventory-log'),

    path('product-list', views.ProductListView.as_view(), name='product-list'),
    path('product/new', views.ProductCreateView.as_view(), name='new-product'),
    path('product/<pk>/edit', views.ProductUpdateView.as_view(), name='edit-product'),
    path('product/<pk>/delete', views.ProductDeleteView.as_view(), name='delete-product'),
    path('purchase-reqd/', views.InventoryPurchaseRequiredView.as_view(), name='purchases-reqd-list'),

    ]