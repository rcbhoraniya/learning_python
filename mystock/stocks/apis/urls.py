from django.urls import path,include
from rest_framework.routers import DefaultRouter
from ..apis.views import *

router = DefaultRouter()
router.register('',StockMapViewSet,basename='stockmap')

urlpatterns=[
    path('',include(router.urls))
]