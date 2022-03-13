from django.urls import path
from .views import *
from django.conf.urls import url,include
from rest_framework import routers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'production', PlantProductionViewSets)
router.register(r'product', ProductViewSets)
router.register(r'plant', PlantViewSets)
router.register(r'order', OrderViewSets)
router.register(r'employee', EmployeeViewSets)
router.register(r'user', UserViewSets)
router.register(r'designation', DesignationViewSets)

urlpatterns = [
    path('', include(router.urls)),
    path('lastreading/',GetLastReadingView.as_view()),
    path('api-token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api-token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api-token/', CustomAuthToken.as_view(), name='api_token_auth'),
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
