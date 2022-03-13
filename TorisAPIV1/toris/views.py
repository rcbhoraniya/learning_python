from .serializers import *
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from .models import *
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from django.contrib.auth.models import User
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
import pandas as pd
import numpy as np
from django.db.models import Avg, Max, Min, Sum, Count, F
from django.views.generic import ListView
import json

pd.set_option('display.width', 1500)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 50)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email
        })


class AllPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserViewSets(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PlantProductionViewSets(viewsets.ModelViewSet):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.DjangoModelPermissions]
    pagination_class = AllPagination
    queryset = PlantProduction.objects.all()
    serializer_class = PlantProductionSerializer
    detail_serializer_class = PlantProductionDetailSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['plant__name', 'date']

    def perform_destroy(self, instance):
        instance.soft_delete()

    def get_queryset(self):
        queryset = PlantProduction.objects.all().order_by('-id')
        return queryset

    def get_serializer_class(self):
        """
        Determins which serializer to use `list` or `detail`
        """
        if self.action == 'list':
            if hasattr(self, 'detail_serializer_class'):
                return self.detail_serializer_class
        return super().get_serializer_class()


class ProductionOrderReportView(APIView):

    def get(self, request, format=None):
        product = Product.objects.all()
        order = Order.objects.all()
        production = PlantProduction.objects.all()
        product = product.values()
        order = order.values()
        production = production.values()
        product_df = pd.DataFrame.from_records(product)
        product_df = product_df.drop(columns=['deleted_at'])
        order_df = pd.DataFrame.from_records(order)
        production_df = pd.DataFrame.from_records(production).drop(
            columns=['id', 'wastage', 'date', 'plant_id', 'shift', 'no_of_winderman', 'operator_name_id', 'deleted_at',
                     ])
        production_df['net_p'] = production_df['end_reading'] - production_df['start_reading']
        production_df = production_df.groupby(['product_code_id'], as_index=False).agg({'net_p': sum})
        order_df = order_df.drop(columns=['deleted_at', 'id', 'order_date', 'customer_name_id', 'pi_number'])
        order_df = order_df.groupby(['product_code_id'], as_index=False).agg({'order_qty': sum})
        production_order = production_df.merge(order_df, left_on='product_code_id', right_on='product_code_id',
                                               how='outer')
        production_order = production_order.replace([np.nan], 0)
        production_order['req_production'] = production_order['order_qty'] - production_order['net_p']
        production_order = production_order.merge(product_df, left_on='product_code_id', right_on='product_code',
                                                  how='left')
        production_order = production_order.drop(columns=['product_code_id', 'net_p', 'order_qty',
                                                          'id'])
        production_order = production_order[production_order['req_production'] != 0]
        production_order = production_order.to_json(orient="records")
        parsed = json.loads(production_order)
        return Response(parsed)


class GetLastReadingView(APIView):

    def get(self, request, format=None):
        plant_id = request.GET.get('plant')
        data = PlantProduction.objects.filter(plant=plant_id).order_by('end_reading').last()
        serializer = PlantProductionSerializer(data)
        return Response(serializer.data)


class ProductViewSets(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all().order_by('product_code')
    serializer_class = ProductSerializer

    def perform_destroy(self, instance):
        instance.soft_delete()


class StatesViewSets(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = State.objects.all().order_by('name')
    serializer_class = StateSerializer

    def perform_destroy(self, instance):
        instance.soft_delete()


class DistrictsViewSets(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = District.objects.all().order_by('name')
    serializer_class = DistrictsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['state_id']

    def perform_destroy(self, instance):
        instance.soft_delete()


class CustomersViewSets(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Customer.objects.all().order_by('name')
    serializer_class = CustomersSerializer

    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['state_id']

    def perform_destroy(self, instance):
        instance.soft_delete()


class OrderViewSets(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_destroy(self, instance):
        instance.soft_delete()


class EmployeeViewSets(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    detail_serializer_class = EmployeeDetailSerializer

    def perform_destroy(self, instance):
        instance.soft_delete()
    def get_queryset(self):
        queryset = Employee.objects.all().order_by('name')
        return queryset

    def get_serializer_class(self):
        """
        Determins which serializer to use `list` or `detail`
        """
        if self.action == 'list':
            if hasattr(self, 'detail_serializer_class'):
                return self.detail_serializer_class
        return super().get_serializer_class()


class DesignationViewSets(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer

    def perform_destroy(self, instance):
        instance.soft_delete()


class PlantViewSets(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer

    def perform_destroy(self, instance):
        instance.soft_delete()

# class PlantProductionList(generics.ListCreateAPIView):
#     pagination_class = AllPagination
#     queryset = PlantProduction.objects.all().order_by('date')
#     serializer_class = PlantProductionSerializer
#
#
# class PlantProductionDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = PlantProduction.objects.all()
#     serializer_class = PlantProductionSerializer
#
#     def perform_destroy(self, instance):
#         instance.soft_delete()


# class ProductList(generics.ListCreateAPIView):
#     queryset = Product.objects.all().order_by('id')
#     serializer_class = ProductSerializer
#
#
# class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#     def perform_destroy(self, instance):
#         instance.soft_delete()


# class OrderList(generics.ListCreateAPIView):
#     queryset = Order.objects.all().order_by('id')
#     serializer_class = OrderSerializer
#
#
# class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#
#     def perform_destroy(self, instance):
#         instance.soft_delete()


# class OperatorList(generics.ListCreateAPIView):
#     queryset = Operator.objects.all().order_by('id')
#     serializer_class = OperatorSerializer
#
#
# class OperatorDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Operator.objects.all()
#     serializer_class = OperatorSerializer
#
#     def perform_destroy(self, instance):
#         instance.soft_delete()


# class PlantList(generics.ListCreateAPIView):
#     queryset = Plant.objects.all()
#     serializer_class = PlantSerializer
#
#
# class PlantDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Plant.objects.all()
#     serializer_class = PlantSerializer
#
#     def perform_destroy(self, instance):
#         instance.soft_delete()

# def load_start_reading(request):
#     plant_id = request.GET.get('plant')
#     query = PlantProduction.objects.filter(plant=plant_id).order_by('end_reading').last()
#     # print(query)
#     end_reading = query.end_reading
#     # print(end_reading)
#     return HttpResponse(json.dumps(end_reading), content_type='application/json')
