import django_tables2 as tables
from django.utils.html import format_html

from .models import *
import itertools

class SummingColumn(tables.Column):
    def render_footer(self, bound_column, table):
        return sum(bound_column.accessor.resolve(row) for row in table.data)


class StockTable(tables.Table):
    DETAIL = """<a class="text-success" href="{% url 'stocks:detail_s' record.id %}">View</a>"""
    view = tables.TemplateColumn(DETAIL, orderable=False, exclude_from_export=True)

    sr = tables.Column(empty_values=(), orderable=False)
    company_name = tables.Column(accessor='portfoliodata')
    company = tables.Column(accessor='company_id')

    nse_symbol = tables.Column(accessor='company__nse_symbol')
    sector = tables.Column(accessor='company__sector')
    total_quantity = tables.Column(accessor='qty_sum')
    # total_price = SummingColumn(accessor='price_sum')
    average_price = tables.Column(accessor='avg_price')
    # id = tables.Column()
    class Meta:
        # model = StockData
        template_name = "django_tables2/bootstrap4.html"
        # fields = ('id',)
        # sequence = ('row_number', 'date','company','nse_name','side','quantity','price','qty_change','price_change')
        attrs = {"class": "table table-bordered table-hover table-sm "}

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.counter = itertools.count()
    #
    # def render_row_number(self):
    #     return "%d" % next(self.counter)
    #
    def render_company(self, value):
        return "%s" % value

    def render_sr(self):
        self.row_sr = getattr(self, 'row_sr',
                              itertools.count(self.page.start_index()))
        return next(self.row_sr)

    def render_average_price(self, value):
        return '{:0.2f}'.format(value)



class SoldStockTable(tables.Table):
    sr = tables.Column(empty_values=(), orderable=False)
    company_name = tables.Column(accessor='company__company_name')
    nse_symbol = tables.Column(accessor='company__nse_symbol')
    sector = tables.Column(accessor='company__sector')
    total_quantity = tables.Column(accessor='qty_sum')
    total_profit = SummingColumn(accessor='price_sum')


    class Meta:

        template_name = "django_tables2/bootstrap4.html"
        attrs = {"class": "table table-bordered table-hover table-sm "}
    def render_sr(self):
        self.row_sr = getattr(self, 'row_sr',
                              itertools.count(self.page.start_index()))
        return next(self.row_sr)

    def render_total_profit(self, value):
        return '{:0.2f}'.format(value)