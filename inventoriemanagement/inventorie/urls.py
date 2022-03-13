from django.urls import path
from . import views

from django.contrib.auth import views as auth_views


app_name = 'stocks'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

]
