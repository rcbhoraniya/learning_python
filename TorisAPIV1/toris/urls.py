from django.urls import path
from .views import *
from django.conf.urls import url,include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'production', PlantProductionViewSets)
router.register(r'product', ProductViewSets)
router.register(r'plant', PlantViewSets)
router.register(r'order', OrderViewSets)
router.register(r'operator', OperatorViewSets)


app_name = 'toris'
urlpatterns = [
    path('', include(router.urls)),
    # url('', index, name='index'),
    # path('production/', PlantProductionList.as_view(), name='production'),
    # path('production/<int:pk>/', PlantProductionDetail.as_view(), name='production_detail'),
    # path('product/', ProductList.as_view(), name='product'),
    # path('product/<int:pk>/', ProductDetail.as_view(), name='product_detail'),
    # path('order/', OrderList.as_view(), name='order'),
    # path('order/<int:pk>/', OrderDetail.as_view(), name='order_detail'),
    # path('operator/', OperatorList.as_view(), name='operator'),
    # path('operator/<int:pk>/', OperatorDetail.as_view(), name='operator_detail'),
    # path('plant/', PlantList.as_view(), name='plant'),
    # path('plant/<int:pk>/', PlantDetail.as_view(), name='plant_detail'),
]
