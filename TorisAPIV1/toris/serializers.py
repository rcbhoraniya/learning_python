from rest_framework import serializers
from .models import *


class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        exclude = ['is_deleted', 'deleted_at']


class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        # fields = '__all__'
        exclude = ['is_deleted', 'deleted_at']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['is_deleted', 'deleted_at']


class OrderSerializer(serializers.ModelSerializer):
    # product_code = ProductSerializer(read_only=True)
    class Meta:
        model = Order
        exclude = ['is_deleted', 'deleted_at']


class PlantProductionSerializer(serializers.ModelSerializer):
    plant_name = serializers.CharField(source='plant.name',read_only=True)
    operator_name_name = serializers.CharField(source='operator_name.name',read_only=True)
    product_code_code = serializers.CharField(source='product_code.product_code',read_only=True)
    gramage = serializers.CharField(source='product_code.gramage',read_only=True)
    cutter_spacing = serializers.CharField(source='product_code.cutter_spacing',read_only=True)
    streanth_per_tape_in_kg = serializers.CharField(source='product_code.streanth_per_tape_in_kg',read_only=True)
    elongation_percent = serializers.CharField(source='product_code.elongation_percent',read_only=True)
    tenacity = serializers.CharField(source='product_code.tenacity',read_only=True)
    pp_percent = serializers.CharField(source='product_code.pp_percent',read_only=True)
    filler_percent = serializers.CharField(source='product_code.filler_percent',read_only=True)
    shiner_percent = serializers.CharField(source='product_code.shiner_percent',read_only=True)
    color_percent = serializers.CharField(source='product_code.color_percent',read_only=True)
    tpt_percent = serializers.CharField(source='product_code.tpt_percent',read_only=True)
    uv_percent = serializers.CharField(source='product_code.uv_percent',read_only=True)
    color_name = serializers.CharField(source='product_code.color_name',read_only=True)

    color_marking_on_bobin = serializers.CharField(source='product_code.color_marking_on_bobin',read_only=True)
    tape_color = serializers.CharField(source='product_code.tape_color',read_only=True)
    denier = serializers.CharField(source='product_code.denier',read_only=True)
    production_in_kg = serializers.SerializerMethodField('get_production')
    class Meta:
        # abstract = True
        model = PlantProduction
        exclude = ['is_deleted', 'deleted_at']

    def get_production(self, obj):
        return obj.end_reading - obj.start_reading

# class PlantProductionReadSerializer(PlantProductionSerializer):
#     plant = PlantSerializer(read_only=True)
#     operator_name = OperatorSerializer(read_only=True)
#     product_code = ProductSerializer(read_only=True)
