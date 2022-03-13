from rest_framework import serializers
from .models import *
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
        fields = ['id', 'name']


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'name']


class DistrictsSerializer(serializers.ModelSerializer):
    state = StateSerializer(read_only=True)

    class Meta:
        model = District
        fields = ['id', 'code', 'name', 'state', 'headquarters']


class CustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ['deleted_at']
        depth = 1


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        # fields = '__all__'
        exclude = ['deleted_at']


class EmployeeSerializer(serializers.ModelSerializer):
    designation_name = serializers.CharField(source='designation.designation', read_only=True)
    state_name = serializers.CharField(source='state.name', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'name', 'mname', 'lname', 'city', 'state', 'address',
                  'district', 'mobile1', 'mobile2', 'aadhhar_no', 'designation',
                  'photo_image', 'designation_name', 'state_name', 'district_name']


class EmployeeDetailSerializer(serializers.ModelSerializer):
    designation_name = serializers.CharField(source='designation.designation', read_only=True)
    state_name = serializers.CharField(source='state.name', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)
    state = StateSerializer(read_only=True)
    district = DistrictsSerializer(read_only=True)
    designation = DesignationSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'name', 'mname', 'lname', 'city', 'state', 'address',
                  'district', 'mobile1', 'mobile2', 'aadhhar_no', 'designation',
                  'photo_image', 'designation_name', 'state_name', 'district_name']


class ProductSerializer(serializers.ModelSerializer):
    # orders = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # plant_productions = serializers.PrimaryKeyRelatedField(many=True, read_only=True,)
    class Meta:
        model = Product
        fields = ['id',
                  # 'orders', 'plant_productions',
                  'product_code', 'color_marking_on_bobin', 'tape_color', 'denier',
                  'gramage', 'tape_width', 'cutter_spacing', 'stock_of_bobin', 'streanth_per_tape_in_kg',
                  'elongation_percent',
                  'tenacity', 'pp_percent', 'filler_percent', 'shiner_percent', 'color_percent', 'tpt_percent',
                  'uv_percent', 'color_name']


class OrderSerializer(serializers.ModelSerializer):
    # product_code = ProductSerializer(read_only=True)
    customer_name = CustomersSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'order_date', 'customer_name', 'product_code', 'order_qty',
                  'pi_number']
        # exclude = ['deleted_at']


class PlantProductionSerializer(serializers.ModelSerializer):
    # plant_name = serializers.CharField(source='plant.name', read_only=True)
    # operator_name_name = serializers.CharField(source='operator_name.name', read_only=True)
    # product_code_code = serializers.CharField(source='product_code.product_code', read_only=True)
    # color_marking_on_bobin = serializers.CharField(source='product_code.color_marking_on_bobin', read_only=True)
    # tape_color = serializers.CharField(source='product_code.tape_color', read_only=True)
    # denier = serializers.CharField(source='product_code.denier', read_only=True)
    # production_in_kg = serializers.ReadOnlyField(source='production_field')

    class Meta:
        model = PlantProduction
        fields = ['id',
                  # 'plant_name', 'operator_name_name', 'product_code_code', 'production_in_kg','color_marking_on_bobin','tape_color','denier'
                  'plant', 'date', 'shift', 'operator_name', 'no_of_winderman',
                  'product_code', 'end_reading', 'start_reading', 'wastage',
                  ]


class PlantProductionDetailSerializer(serializers.ModelSerializer):
    plant_name = serializers.CharField(source='plant.name', read_only=True)
    operator_name_name = serializers.CharField(source='operator_name.name', read_only=True)
    product_code_code = serializers.CharField(source='product_code.product_code', read_only=True)
    color_marking_on_bobin = serializers.CharField(source='product_code.color_marking_on_bobin', read_only=True)
    tape_color = serializers.CharField(source='product_code.tape_color', read_only=True)
    denier = serializers.CharField(source='product_code.denier', read_only=True)
    production_in_kg = serializers.ReadOnlyField(source='production_field')
    plant = PlantSerializer(read_only=True)
    operator_name = EmployeeSerializer(read_only=True)
    product_code = ProductSerializer(read_only=True)

    class Meta:
        model = PlantProduction
        fields = ['id', 'plant', 'date', 'shift', 'operator_name', 'no_of_winderman',
                  'product_code', 'end_reading', 'start_reading', 'wastage',
                  'production_in_kg', 'plant_name', 'operator_name_name', 'product_code_code',
                  'color_marking_on_bobin', 'tape_color', 'denier'
                  ]

        # depth = 2
