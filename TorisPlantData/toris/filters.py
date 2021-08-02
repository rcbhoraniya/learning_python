import django_tables2 as tables
from django_filters.widgets import RangeWidget
from .models import PlantProduction, Plant, Product, Order,Operator
import django_filters
from django import forms
from bootstrap_datepicker_plus import DatePickerInput


class DateInput(forms.DateInput):
    input_type = 'date'


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
    production = django_filters.CharFilter(max_length=10, )

    class Meta:
        model = PlantProduction
        fields = ['date', 'plant', 'shift', 'operator_name', 'no_of_winderman', 'product_code', 'start_reading',
                  'end_reading', 'wastage']


class ProductFilter(django_filters.FilterSet):
    req_denier = django_filters.NumberFilter(field_name='req_denier', lookup_expr='gt')

    class Meta:
        model = Product
        fields = ['product_code', 'color_marking_on_bobin', 'tape_color', 'req_denier', 'req_gramage', 'req_tape_width',
                  'cutter_spacing', 'req_streanth_per_tape_in_kg', 'req_elongation_percent', 'streanth', 'tanacity',
                  'pp_percent', 'filler_percent', 'shiner_percent', 'color_percent', 'tpt_percent', 'uv_percent',
                  'color_name']


class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = ['order_date', 'customer_name', 'product_code', 'order_qty']

class OperatorFilter(django_filters.FilterSet):
    class Meta:
        model = Operator
        fields = ['name']