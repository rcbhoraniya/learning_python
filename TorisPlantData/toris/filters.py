import django_tables2 as tables
from django_filters.widgets import RangeWidget
from .models import PlantProduction, Plant, Product, Order,Operator
import django_filters
from django import forms
from bootstrap_datepicker_plus import DatePickerInput


# class DateInput(forms.DateInput):
#     input_type = 'date'


class PlantProductionFilter(django_filters.FilterSet):
    # plant = django_filters.ModelChoiceFilter(queryset=Plant.objects.all())
    # date = django_filters.DateRangeFilter(field_name="date")

    date = django_filters.DateFromToRangeFilter(field_name="date",
                                                # widget=DatePickerInput(format='%d/%m/%Y'),
                                                widget=RangeWidget(attrs={"type": "text", "placeholder": "DD/MM/YYYY"}))
    plant = django_filters.CharFilter(max_length=3, field_name='plant__name', lookup_expr='icontains')
    shift = django_filters.CharFilter(max_length=5, lookup_expr='icontains')
    operator_name = django_filters.CharFilter(max_length=100, field_name='operator_name__name', lookup_expr='icontains')
    product_code = django_filters.CharFilter(max_length=10)
    production_in_kg = django_filters.NumberFilter(field_name='production_in_kg',lookup_expr='lte')

    class Meta:
        model = PlantProduction
        # fields = '__all__'
        exclude = ('is_deleted', 'deleted_at')
        fields = ['date', 'plant', 'shift', 'operator_name', 'product_code', 'start_reading',
                  'end_reading', 'wastage','product_code__denier']


class ProductFilter(django_filters.FilterSet):
    denier = django_filters.NumberFilter(field_name='denier',lookup_expr='gte')


    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('is_deleted', 'deleted_at','stock_of_bobin')
        # fields = ['product_code', 'color_marking_on_bobin', 'tape_color', 'denier', 'gramage', 'tape_width',
        #           'cutter_spacing', 'streanth_per_tape_in_kg', 'elongation_percent',  'tanacity','color_name',
        #           'pp_percent', 'filler_percent', 'shiner_percent', 'color_percent', 'tpt_percent', 'uv_percent',
        #           ]


class OrderFilter(django_filters.FilterSet):
    product_code = django_filters.CharFilter(max_length=10)
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ('is_deleted', 'deleted_at')


class OperatorFilter(django_filters.FilterSet):
    class Meta:
        model = Operator
        fields = '__all__'
        exclude = ('is_deleted', 'deleted_at')