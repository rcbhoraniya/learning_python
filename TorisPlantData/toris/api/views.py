from .serializers import *
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from toris.models import *
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
    queryset = PlantProduction.objects.all().order_by('id')
    serializer_class = PlantProductionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['plant__name', 'date']

    def perform_destroy(self, instance):
        instance.soft_delete()


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


class OrderViewSets(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all().order_by('order_date')
    serializer_class = OrderSerializer

    def perform_destroy(self, instance):
        instance.soft_delete()


class EmployeeViewSets(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Employee.objects.all().order_by('name')
    serializer_class = EmployeeSerializer

    def perform_destroy(self, instance):
        instance.soft_delete()


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
