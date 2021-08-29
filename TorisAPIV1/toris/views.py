from .serializers import *
from rest_framework import generics,viewsets
from .models import *
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination


class AllPagination(PageNumberPagination):
    page_size = 5

    def get_page_size(self, request):
        page_size = request.GET.get('pagesize')
        return page_size

class PlantProductionViewSets(viewsets.ModelViewSet):
    pagination_class = AllPagination
    queryset = PlantProduction.objects.all().order_by('date')
    serializer_class = PlantProductionSerializer

    def perform_destroy(self, instance):
        instance.soft_delete()

class ProductViewSets(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_destroy(self, instance):
        instance.soft_delete()

class OrderViewSets(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_destroy(self, instance):
        instance.soft_delete()

class OperatorViewSets(viewsets.ModelViewSet):
    queryset = Operator.objects.all()
    serializer_class = OperatorSerializer

    def perform_destroy(self, instance):
        instance.soft_delete()

class PlantViewSets(viewsets.ModelViewSet):
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
