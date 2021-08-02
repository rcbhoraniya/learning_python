from django.urls import path
from . import views

app_name = 'toris'
urlpatterns = [
    path('', views.PlantProductionListView.as_view(), name='production_list'),
    # path('sort/plant-production/<str:data>/', views.PlantProductionSortView.as_view(), name='plant_production_sort_list'),
    path('production-create/', views.PlantProductionCreateView.as_view(), name='production_create'),
    path('production-detail/<int:pk>/', views.PlantProductionDetailView.as_view(), name='production_detail'),
    path('production/<int:pk>/update/', views.ProductionUpdateView.as_view(), name='production_update'),
    path('production/<int:pk>/delete/', views.ProductionDeleteView.as_view(), name='production_delete'),
    path('product-list/', views.ProductListView.as_view(), name='product_list'),
    # path('sort/product/<str:data>/', views.ProductSortView.as_view(), name='product_sort_list'),
    path('product-detail/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product-create/', views.ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('order-list/', views.OrderListView.as_view(), name='order_list'),
    # path('sort/order/<str:data>/', views.OrderSortView.as_view(), name='order_sort_list'),
    path('order-detail/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('order-create/', views.OrderCreateView.as_view(), name='order_create'),
    path('order/<int:pk>/update/', views.OrderUpdateView.as_view(), name='order_update'),
    path('order/<int:pk>/delete/', views.OrderDeleteView.as_view(), name='order_delete'),
    path('ajax/load-plant/', views.load_start_reading, name='ajax_load_plant'),  # <-- this one here
    path('operator-detail/<int:pk>/', views.OperatorDetailView.as_view(), name='operator_detail'),
    path('operator-create/', views.OperatorCreateView.as_view(), name='operator_create'),
    path('operator/<int:pk>/update/', views.OperatorUpdateView.as_view(), name='operator_update'),
    path('operator/<int:pk>/delete/', views.OperatorDeleteView.as_view(), name='operator_delete'),
    path('operator-list/', views.OperatorListView.as_view(), name='operator_list'),
    path('production-order/', views.ProductionOrderListView.as_view(), name='production_order_list'),
    path('export/',views.export_production_order_csv, name='export_production_order_csv'),
]
