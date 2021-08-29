from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import *
from django.conf import settings
from django.conf.urls.static import static


app_name = 'toris'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('production_list/', PlantProductionListView.as_view(), name='production_list'),
    path('production-create/', PlantProductionCreateView.as_view(), name='production_create'),
    path('production-detail/<int:pk>/', PlantProductionDetailView.as_view(), name='production_detail'),
    path('production/<int:pk>/update/', ProductionUpdateView.as_view(), name='production_update'),
    path('production/<int:pk>/delete/', ProductionDeleteView.as_view(), name='production_delete'),
    path('product-list/', ProductListView.as_view(), name='product_list'),
    path('product-detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product-create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('order-list/', OrderListView.as_view(), name='order_list'),
    path('order-detail/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('order-create/', OrderCreateView.as_view(), name='order_create'),
    path('order/<int:pk>/update/', OrderUpdateView.as_view(), name='order_update'),
    path('order/<int:pk>/delete/', OrderDeleteView.as_view(), name='order_delete'),
    path('ajax/load-plant/', load_start_reading, name='ajax_load_plant'),  # <-- this one here
    path('operator-detail/<int:pk>/', OperatorDetailView.as_view(), name='operator_detail'),
    path('operator-create/', OperatorCreateView.as_view(), name='operator_create'),
    path('operator/<int:pk>/update/', OperatorUpdateView.as_view(), name='operator_update'),
    path('operator/<int:pk>/delete/', OperatorDeleteView.as_view(), name='operator_delete'),
    path('operator-list/', OperatorListView.as_view(), name='operator_list'),
    path('production-order/', ProductionOrderListView.as_view(), name='production_order_list'),
    path('export/',export_production_order_csv, name='export_production_order_csv'),

    path("register", UserRegistrationView.as_view(), name="register"),
    path("no-permission", PermissionDeniedView.as_view(), name="permissiondenied"),
    path('login/', auth_views.LoginView.as_view(template_name = 'toris/login.html'),name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name ='toris/password_change.html',
                                                                   success_url = '/change-password-done/'), name='password_change'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name ='toris/password_reset.html'),name = 'password_reset'),
    path('change-password-done/', auth_views.PasswordChangeDoneView.as_view(template_name ='toris/change_password_done.html'), name='change-password-done'),
]

