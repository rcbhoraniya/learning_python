from ..models import *
from rest_framework import serializers

class StockMapSerializer(serializers.ModelSerializer):
    class Meta:
        model=StockMap
        fields = ['id','company_name','nse_symbol']