import django_tables2 as tables
from .models import PlantProduction, Plant, Product, Order,Operator


class SummingColumn(tables.Column):
    def render_footer(self, bound_column, table):
        return sum(bound_column.accessor.resolve(row) for row in table.data)


class PlantProductionTable(tables.Table):
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
    production = SummingColumn()
    wastage = SummingColumn()

    class Meta:
        model = PlantProduction
        template_name = "django_tables2/bootstrap4.html"
        fields = (
        'date', 'plant', 'shift', 'operator_name', 'no_of_winderman', 'product_code', 'start_reading', 'end_reading',
        'production', 'wastage')
        attrs = {"class": "table table-hover table-sm"}


class ProductTable(tables.Table):
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
        fields = ('product_code', 'color_marking_on_bobin', 'tape_color', 'req_denier', 'req_gramage', 'req_tape_width',
                  'cutter_spacing', 'req_streanth_per_tape_in_kg', 'req_elongation_percent', 'streanth', 'tanacity',
                  'pp_percent', 'filler_percent', 'shiner_percent', 'color_percent', 'tpt_percent', 'uv_percent',
                  'color_name')
        attrs = {"class": "table table-hover table-sm"}


class OrderTable(tables.Table):
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
        fields = ('order_date', 'customer_name', 'product_code', 'order_qty')
        attrs = {"class": "table table-hover table-sm"}

class ProductionOrderTable(tables.Table):
    # DELETE = """
    # <a href="{% url 'toris:order_delete' record.id  %}"><i
    #                     class="far fa-trash-alt  text-danger"></i></a>
    #  """
    # EDIT = """<a href="{% url 'toris:order_update' record.id %}"><i class="fas fa-edit "></i></a>"""
    # DETAIL = """<a class="text-success" href="{% url 'toris:order_detail' record.id %}">View</a>"""
    # View = tables.TemplateColumn(DETAIL, orderable=False, exclude_from_export=True)
    # Edit = tables.TemplateColumn(EDIT, orderable=False, exclude_from_export=True)
    # Delete = tables.TemplateColumn(DELETE, orderable=False, exclude_from_export=True)
    order_date = tables.Column()
    product_code = tables.Column()
    customer_name = tables.Column()
    order_qty = tables.Column()
    class Meta:
        model = Order
        template_name = "django_tables2/bootstrap4.html"
        fields = ('order_date', 'customer_name', 'product_code', 'order_qty')
        attrs = {"class": "table table-hover table-sm"}

class OperatorTable(tables.Table):
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
        model = Operator
        template_name = "django_tables2/bootstrap4.html"
        fields = ('name',)
        attrs = {"class": "table table-hover table-sm"}