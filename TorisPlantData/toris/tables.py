import django_tables2 as tables
from .models import PlantProduction, Plant, Product, Order, Employee
import itertools


class SummingColumn(tables.Column):
    def render_footer(self, bound_column, table):
        return sum(bound_column.accessor.resolve(row) for row in table.data)


class PlantProductionTable(tables.Table):
    sr = tables.Column(empty_values=(), orderable=False)
    DELETE = """
    <a href="{% url 'toris:production_delete' record.id  %}"><i
                        class="far fa-trash-alt  text-danger"></i></a>
     """
    EDIT = """<a href="{% url 'toris:production_update' record.id %}"><i class="fas fa-edit "></i></a>"""
    DETAIL = """<a class="text-success" href="{% url 'toris:production_detail' record.id %}">View</a>"""
    # id = tables.LinkColumn('toris:production_detail', args=[A('pk')])
    View = tables.TemplateColumn(DETAIL, orderable=False, exclude_from_export=True)
    Edit = tables.TemplateColumn(EDIT, orderable=False, exclude_from_export=True)
    Delete = tables.TemplateColumn(DELETE, orderable=False, exclude_from_export=True)
    date = tables.DateTimeColumn(format='d/m/Y')
    end_reading = tables.Column(footer="Total:")
    production_in_kg = SummingColumn()
    wastage = SummingColumn()

    # color_marking_on_bobin = tables.Column()
    class Meta:
        model = PlantProduction
        template_name = "toris/table.html"

        # template_name = "django_tables2/bootstrap4.html"
        fields = ('sr', 'date', 'plant', 'shift', 'operator_name', 'no_of_winderman', 'product_code',
                  'product_code__color_marking_on_bobin', 'product_code__tape_color', 'product_code__denier',
                  'start_reading', 'end_reading', 'production_in_kg', 'wastage',)
        attrs = {"class": "table table-bordered table-hover table-sm ",

                 }

    def render_sr(self):
        self.row_sr = getattr(self, 'row_sr',
                              itertools.count(self.page.start_index()))
        return next(self.row_sr)


class ProductTable(tables.Table):
    sr = tables.Column(empty_values=(), orderable=False)
    DELETE = """
    <a href="{% url 'toris:product_delete' record.id  %}"><i
                        class="far fa-trash-alt  text-danger"></i></a>
     """
    EDIT = """<a href="{% url 'toris:product_update' record.id %}"><i class="fas fa-edit "></i></a>"""
    DETAIL = """<a class="text-success" href="{% url 'toris:product_detail' record.id %}">View</a>"""
    View = tables.TemplateColumn(DETAIL, orderable=False, exclude_from_export=True)
    Edit = tables.TemplateColumn(EDIT, orderable=False, exclude_from_export=True)
    Delete = tables.TemplateColumn(DELETE, orderable=False, exclude_from_export=True)

    class Meta:
        model = Product
        template_name = "django_tables2/bootstrap4.html"
        fields = ('sr', 'product_code', 'color_marking_on_bobin', 'tape_color', 'denier', 'gramage', 'tape_width',
                  'cutter_spacing', 'streanth_per_tape_in_kg', 'elongation_percent', 'tanacity',
                  'pp_percent', 'filler_percent', 'shiner_percent', 'color_percent', 'tpt_percent', 'uv_percent',
                  'color_name')
        attrs = {"class": "table table-bordered table-hover table-sm "}

    def render_sr(self):
        self.row_sr = getattr(self, 'row_sr',
                              itertools.count(self.page.start_index()))
        return next(self.row_sr)


class OrderTable(tables.Table):
    sr = tables.Column(empty_values=(), orderable=False)
    DELETE = """
    <a href="{% url 'toris:order_delete' record.id  %}"><i
                        class="far fa-trash-alt  text-danger"></i></a>
     """
    EDIT = """<a href="{% url 'toris:order_update' record.id %}"><i class="fas fa-edit "></i></a>"""
    DETAIL = """<a class="text-success" href="{% url 'toris:order_detail' record.id %}">View</a>"""
    View = tables.TemplateColumn(DETAIL, orderable=False, exclude_from_export=True)
    Edit = tables.TemplateColumn(EDIT, orderable=False, exclude_from_export=True)
    Delete = tables.TemplateColumn(DELETE, orderable=False, exclude_from_export=True)

    class Meta:
        model = Order
        template_name = "django_tables2/bootstrap4.html"
        fields = ('sr', 'order_date', 'customer_name', 'product_code',
                  'product_code__color_marking_on_bobin', 'product_code__tape_color', 'product_code__denier',
                  'order_qty', 'pi_number')
        attrs = {"class": "table table-bordered table-hover table-sm "}

    def render_sr(self):
        self.row_sr = getattr(self, 'row_sr',
                              itertools.count(self.page.start_index()))
        return next(self.row_sr)


class EmployeeTable(tables.Table):
    sr = tables.Column(empty_values=(), orderable=False)
    DELETE = """
    <a href="{% url 'toris:operator_delete' record.id  %}"><i
                        class="far fa-trash-alt  text-danger"></i></a>
     """
    EDIT = """<a href="{% url 'toris:operator_update' record.id %}"><i class="fas fa-edit "></i></a>"""
    DETAIL = """<a class="text-success" href="{% url 'toris:operator_detail' record.id %}">View</a>"""
    View = tables.TemplateColumn(DETAIL, orderable=False, exclude_from_export=True)
    Edit = tables.TemplateColumn(EDIT, orderable=False, exclude_from_export=True)
    Delete = tables.TemplateColumn(DELETE, orderable=False, exclude_from_export=True)

    class Meta:
        model = Employee
        template_name = "django_tables2/bootstrap4.html"
        fields = ('sr', 'id', 'name',)
        attrs = {"class": "table table-bordered table-hover table-sm "}

    def render_sr(self):
        self.row_sr = getattr(self, 'row_sr',
                              itertools.count(self.page.start_index()))
        return next(self.row_sr)
