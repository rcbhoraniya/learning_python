import django_tables2 as tables
from django.forms import DateInput
from django_filters.widgets import RangeWidget

from .models import PlantProduction,Plant
from django_tables2.utils import A
import django_filters
from bootstrap_datepicker_plus import DatePickerInput
from django_tables2.export.export import TableExport
class PlantProductionFilter(django_filters.FilterSet):

    id = django_filters.CharFilter(max_length=10)
    # plant = django_filters.ModelChoiceFilter(queryset=Plant.objects.all())
    # date = django_filters.DateRangeFilter(field_name="date")

    date = django_filters.DateFromToRangeFilter(field_name="date",
                                                # widget=DatePickerInput(format='%d/%m/%Y'),
                                                widget=RangeWidget(attrs={"type": "text", "placeholder": "DD/MM/YYYY"})
                                                )
    shift = django_filters.CharFilter(max_length=5,lookup_expr='icontains')
    operator_name = django_filters.CharFilter(max_length=100,field_name='operator_name__name',lookup_expr='icontains')
    product_code = django_filters.CharFilter(max_length=10)
    Plant = django_filters.CharFilter(max_length=3, field_name='plant__name', lookup_expr='icontains')

    class Meta:
        model = PlantProduction
        fields = ['id','date','shift','operator_name','no_of_winderman','product_code','end_reading','start_reading','wastage']

class SummingColumn(tables.Column):
    def render_footer(self, bound_column, table):
        return sum(bound_column.accessor.resolve(row) for row in table.data)


class PlantProductionTable(tables.Table):
    DELETE = """
    <a href="{% url 'toris:production_delete' record.id  %}"><i
                        class="far fa-trash-alt fa-lg text-danger"></i></a>
     """
    EDIT = """<a href="{% url 'toris:production_update' record.id %}"><i class="fas fa-edit fa-lg"></i></a>"""
    DETAIL = """<a class="text-success" href="{% url 'toris:production_detail' record.id %}">View</a>"""
    # id = tables.LinkColumn('toris:production_detail', args=[A('pk')])
    View = tables.TemplateColumn(DETAIL,orderable=False,exclude_from_export=True)
    Edit = tables.TemplateColumn(EDIT,orderable=False,exclude_from_export=True)
    Delete = tables.TemplateColumn(DELETE,orderable=False,exclude_from_export=True)
    date = tables.DateTimeColumn(format ='d/m/Y')
    end_reading = tables.Column(footer="Total:")
    production = SummingColumn()
    wastage = SummingColumn()

    class Meta:
        model = PlantProduction
        template_name = "django_tables2/bootstrap4.html"
        fields = ('date','plant','shift','operator_name','no_of_winderman','product_code','start_reading','end_reading','production','wastage')
        attrs = {"class": "table table-hover table-sm"}
