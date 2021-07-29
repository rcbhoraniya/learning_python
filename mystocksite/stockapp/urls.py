from django.urls import path

from . import views

app_name = 'stockapp'
urlpatterns = [
    path('', views.StockListView.as_view(), name='stock-list'),
    path('search/', views.SearchView.as_view(), name='search_results'),
    path('<int:id>/<nse_symbol>/', views.StockDetailListView.as_view(), name='detail'),
    path('stock/add/', views.AddStockFormView.as_view(), name='stock-add'),

]