from rest_framework import serializers
from toris.models import *
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user'] = str(self.user.username)

        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        exclude = ['is_deleted', 'deleted_at']


class EmployeeSerializer(serializers.ModelSerializer):
    designation_name = serializers.CharField(source='designation.designation', read_only=True)
    class Meta:
        model = Employee
        # fields = '__all__'
        exclude = ['is_deleted', 'deleted_at']

class DesignationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Designation
        # fields = '__all__'
        exclude = ['is_deleted', 'deleted_at']


class ProductSerializer(serializers.ModelSerializer):
    orders = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    plant_productions = serializers.PrimaryKeyRelatedField(many=True, read_only=True,)
    class Meta:
        model = Product
        fields=['id','orders','plant_productions','product_code','color_marking_on_bobin','tape_color','denier',
                'gramage','tape_width','cutter_spacing','stock_of_bobin','streanth_per_tape_in_kg','elongation_percent',
                'tenacity','pp_percent','filler_percent','shiner_percent','color_percent','tpt_percent','uv_percent','color_name']



class OrderSerializer(serializers.ModelSerializer):
    # product_code = ProductSerializer(read_only=True)
    class Meta:
        model = Order
        exclude = ['is_deleted', 'deleted_at']


class PlantProductionSerializer(serializers.ModelSerializer):
    plant_name = serializers.CharField(source='plant.name', read_only=True)
    operator_name_name = serializers.CharField(source='operator_name.name', read_only=True)
    product_code_code = serializers.CharField(source='product_code.product_code', read_only=True)
    gramage = serializers.CharField(source='product_code.gramage', read_only=True)
    cutter_spacing = serializers.CharField(source='product_code.cutter_spacing', read_only=True)
    streanth_per_tape_in_kg = serializers.CharField(source='product_code.streanth_per_tape_in_kg', read_only=True)
    elongation_percent = serializers.CharField(source='product_code.elongation_percent', read_only=True)
    tenacity = serializers.CharField(source='product_code.tenacity', read_only=True)
    pp_percent = serializers.CharField(source='product_code.pp_percent', read_only=True)
    filler_percent = serializers.CharField(source='product_code.filler_percent', read_only=True)
    shiner_percent = serializers.CharField(source='product_code.shiner_percent', read_only=True)
    color_percent = serializers.CharField(source='product_code.color_percent', read_only=True)
    tpt_percent = serializers.CharField(source='product_code.tpt_percent', read_only=True)
    uv_percent = serializers.CharField(source='product_code.uv_percent', read_only=True)
    color_name = serializers.CharField(source='product_code.color_name', read_only=True)

    color_marking_on_bobin = serializers.CharField(source='product_code.color_marking_on_bobin', read_only=True)
    tape_color = serializers.CharField(source='product_code.tape_color', read_only=True)
    denier = serializers.CharField(source='product_code.denier', read_only=True)
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
