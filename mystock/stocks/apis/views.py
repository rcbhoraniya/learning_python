from ..models import *
from ..apis.serializers import StockMapSerializer
from rest_framework import viewsets

class StockMapViewSet(viewsets.ModelViewSet):
    queryset = StockMap.objects.all()
    serializer_class = StockMapSerializer