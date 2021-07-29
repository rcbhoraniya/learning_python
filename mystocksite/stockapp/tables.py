# # tutorial/tables.py
# import django_tables2 as tables
# from .models import Stock,Stock_price
# from django.utils.html import format_html
#
# class StockTable(tables.Table):
#     name = tables.Column()
#
#     class Meta:
#         # model = Stock
#         template_name = "django_tables2/bootstrap.html"
#
#     def render_name(self, record):
#
#         return format_html("<a href={}> {}</a>",record.id ,record.nse_symbol)
#
# class StockTableDetail(tables.Table):
#     name = tables.Column()
#
#     class Meta:
#         # model = Stock
#         template_name = "django_tables2/bootstrap.html"
#
#     def render_name(self, record):
#
#         return format_html("<h3>{} {} {} </h3>",record.open,record.high,record.low)