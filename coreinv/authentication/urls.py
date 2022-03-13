from django.urls import path
# from django.conf.urls import url
from .views import UserLoginView,UserLogoutView,PermissionDeniedView
app_name = 'authentication'
urlpatterns = [
    path('', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path("no-permission", PermissionDeniedView.as_view(), name="permissiondenied"),

]