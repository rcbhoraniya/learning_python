from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'stocks'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('portfolio-detail/<int:pk>/', views.StockDetailView.as_view(), name='portfolio_detail'),
    path('historicaldata/<int:pk>/', views.HistoricalDataView.as_view(), name='historicaldata'),
    path('sector-analysis/', views.SectorAnalysis.as_view(), name='sector_analysis'),
    path('market-cap-analysis/', views.MarketCapAnalysis.as_view(), name='marketcap_analysis'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('refresh-price/', views.refresh_price_data, name='refresh_price'),

    path('bulk_create/', views.BulkCreateHistoricalData, name='bulk_create_historicaldata'),
    path('bulk_stockdata/', views.bulkCreateStockData, name='bulk_create_stockdata'),
    path('bulk_nsehist/', views.BulkCreateNSEHistorical, name='bulk_create_nsehist'),
    path('bulk_bhavcopy/', views.BulkCreateNSEBhavcopy, name='bulk_create_bhavcopy'),
    path('export/', views.export_data_csv, name='exportcsv'),

    path('stockmap-list/', views.StockMapListView.as_view(), name='stockmap_list'),
    path('stockmap-detail/<int:pk>/', views.StockMapDetailView.as_view(), name='stockmap_detail'),
    path('stockmap-add/', views.StockMapCreateView.as_view(), name='stockmap_add'),
    path('stockmap-update/<int:pk>', views.StockMapUpdateView.as_view(), name='stockmap_update'),
    path('stockmap-delete/<int:pk>', views.StockMapDeleteView.as_view(), name='stockmap_delete'),

    path('sector-stock/<sector>', views.SectorStockListView.as_view(), name='sector_stock'),

    path('sector-list/', views.SectorListView.as_view(), name='sector_list'),
    path('sector-detail/<int:pk>/', views.SectorDetailView.as_view(), name='sector_detail'),
    path('sector-add/', views.SectorCreateView.as_view(), name='sector_add'),
    path('sector-update/<int:pk>', views.SectorUpdateView.as_view(), name='sector_update'),
    path('sector-delete/<int:pk>', views.SectorDeleteView.as_view(), name='sector_delete'),

    path('stockdata-list/', views.StockDataListView.as_view(), name='stockdata_list'),
    path('stockdata-detail/<int:pk>/', views.StockDataDetailView.as_view(), name='stockdata_detail'),
    path('stockdata-add/', views.StockDataCreateView.as_view(), name='stockdata_add'),
    path('stockdata-update/<int:pk>', views.StockDataUpdateView.as_view(), name='stockdata_update'),
    path('stockdata-delete/<int:pk>', views.StockDataDeleteView.as_view(), name='stockdata_delete'),

    path('historicaldata-list/', views.HistoricalDataListView.as_view(), name='historicaldata_list'),
    path('historicaldata-detail/<int:pk>/', views.HistoricalDataDetailView.as_view(), name='historicaldata_detail'),
    path('historicaldata-add/', views.HistoricalDataCreateView.as_view(), name='historicaldata_add'),
    path('historicaldata-update/<int:pk>', views.HistoricalDataUpdateView.as_view(), name='historicaldata_update'),
    path('historicaldata-delete/<int:pk>', views.HistoricalDataDeleteView.as_view(), name='historicaldata_delete'),

    path("register", views.UserRegistrationView.as_view(), name="register"),
    path("no-permission", views.PermissionDeniedView.as_view(), name="permissiondenied"),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='stocks/password_change.html',
                                                                   success_url='/change-password-done/'),
         name='password_change'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='stocks/password_reset.html'),
         name='password_reset'),
    path('change-password-done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='stocks/change_password_done.html'),
         name='change-password-done'),

]
