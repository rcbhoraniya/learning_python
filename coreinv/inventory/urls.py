from django.urls import path
# from django.conf.urls import url
from django.views.generic.dates import ArchiveIndexView
from .models import Invoice,PurchaseInvoice
from . import views
app_name = 'inventory'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about', views.AboutView.as_view(), name='about'),

    path('stock-list', views.StockListView.as_view(), name='stock-list'),
    path('stock/new', views.StockCreateView.as_view(), name='new-stock'),
    path('stock/<pk>/edit', views.StockUpdateView.as_view(), name='edit-stock'),
    path('stock/<pk>/delete', views.StockDeleteView.as_view(), name='delete-stock'),

    path('product-list', views.ProductListView.as_view(), name='product-list'),
    path('product/new', views.ProductCreateView.as_view(), name='new-product'),
    path('product/<pk>/edit', views.ProductUpdateView.as_view(), name='edit-product'),
    path('product/<pk>/delete', views.ProductDeleteView.as_view(), name='delete-product'),

    path('supplier-list', views.SupplierListView.as_view(), name='supplier-list'),
    path('supplier/new', views.SupplierCreateView.as_view(), name='new-supplier'),
    path('supplier/<pk>/edit', views.SupplierUpdateView.as_view(), name='edit-supplier'),
    path('supplier/<pk>/delete', views.SupplierDeleteView.as_view(), name='delete-supplier'),
    path('supplier/<name>', views.SupplierBillListView.as_view(), name='supplier-bill-list'),

    path('purchase-bill-list', views.PurchaseBillListView.as_view(), name='purchase-bill-list'),
    path('purchase-reqd/', views.StockPurchaseRequiredView.as_view(), name='purchases-reqd-list'),
    path('purchase/new', views.PurchaseCreateView.as_view(), name='new-purchase'),
    path('purchasebill/<int:purchaseinvoice_number>', views.PurchaseBillViewer.as_view(), name='purchasebill_viewer'),
    path('purchase/<pk>/delete', views.PurchaseDeleteView.as_view(), name='delete-purchase'),
    # path('purchases/<pk>/delete', views.PurchaseDeleteView.as_view(), name='delete-purchase'),

    path('sales-bill-list', views.SalseBillListView.as_view(), name='sales-bill-list'),
    path('sales/new', views.SalesBillCreateView.as_view(), name='new-sales'),
    path('salesbill/<int:invoice_number>', views.SalseBillViewer.as_view(), name='salesbill_viewer'),
    path('sales/<pk>/delete', views.SalesDeleteView.as_view(), name='delete-sale'),

    # path('purchases/<pk>/delete', views.PurchaseDeleteView.as_view(), name='delete-purchase'),

    path('customer-list/', views.CustomerListView.as_view(), name='customer-list'),
    path('customer/new',views.CustomerCreateView.as_view(), name='new-customer'),
    path('customer/<pk>/edit', views.CustomerUpdateView.as_view(), name='edit-customer'),
    path('customer/<pk>/delete', views.CustomerDeleteView.as_view(), name='delete-customer'),
    path('customer/<name>', views.CustomerBillListView.as_view(), name='customer-bill-list'),

    path('archive/',ArchiveIndexView.as_view(model=Invoice, date_field="date",template_name='archive/invoice_archive.html'), name="invoice_archive"),
    path('<int:year>/',views.InvoiceYearArchiveView.as_view(),name="article_year_archive"),
    # Example: /2012/08/
    path('<int:year>/<int:month>/', views.InvoiceMonthArchiveView.as_view(month_format='%m'), name="archive_month_numeric"),
    # Example: /2012/aug/
    path('<int:year>/<str:month>/',views.InvoiceMonthArchiveView.as_view(), name="archive_month"),


    path('productsjson', views.productsjson, name='productsjson'),
    path('suppliersjson', views.suppliersjson, name='suppliersjson'),
    path('customersjson', views.customersjson, name='customersjson'),
    path('customerjson', views.customerjson, name='customerjson'),
    path('productjson', views.productjson, name='productjson'),

    ]