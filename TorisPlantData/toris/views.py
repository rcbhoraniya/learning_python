from django.urls import reverse_lazy
import json
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from .models import Product, PlantProduction, Order
from django.http import HttpResponseRedirect, HttpResponse
from .forms import PlantProductionForm, ProductForm, OrderForm
from django.db.models import Avg, Max, Min, Sum, Count, F
import pandas as pd
import numpy as np
import csv
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render
from django.views import View
from datetime import date, datetime, timedelta
from django.db.models import OuterRef, Subquery
from django.db.models.functions import Lower
from django.db import connection
from django_tables2 import SingleTableView
from django_tables2 import SingleTableView
from .tables import PlantProductionTable,PlantProductionFilter
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_tables2.export.views import ExportMixin
from django_tables2.export.export import TableExport
class PlantProductionListView(ExportMixin,SingleTableMixin, FilterView):
    model = PlantProduction
    table_class = PlantProductionTable
    template_name = 'toris/index.html'
    filterset_class = PlantProductionFilter
    table_pagination = {"per_page": 50 }
    export_formats = ['xlsx', 'csv']

    def get_queryset(self):
        qs = self.model.objects.all().annotate(production =(F('end_reading') - F('start_reading')))
        filtered_list = PlantProductionFilter(self.request.GET, queryset=qs)
        return filtered_list.qs
# class PlantProductionListView(ListView):
#     model = PlantProduction
#     template_name = 'toris/index.html'
#     context_object_name = 'productionall'
#     paginate_by = 20
    # success_url = reverse_lazy('toris:production_list')

    # def get_queryset(self):
    #     production_list = PlantProduction.plant_production.all()
    #     print(production_list.query)
    #     return production_list
    # def get_queryset(self,*args,**kwargs):
    #     production_list = PlantProduction.objects.order_by(self.kwargs.get('date'))
    #     return production_list


class PlantProductionSortView(ListView):
    model = PlantProduction
    template_name = 'toris/index.html'
    context_object_name = 'productionall'
    paginate_by = 20
    success_url = reverse_lazy('toris:production_list')

    def get_queryset(self, *args, **kwargs):
        production_list = PlantProduction.objects.order_by(self.kwargs.get('data'))
        return production_list


class PlantProductionCreateView(CreateView):
    model = PlantProduction
    form_class = PlantProductionForm
    template_name = 'toris/plant-production-add.html'
    success_url = reverse_lazy('toris:production_list')


def load_start_reading(request):
    plant_id = request.GET.get('plant')
    # print(plant_id)
    # if plant_id == 'TPF':
    #     plant_id = 'TPF'
    # elif plant_id == 'TPP':
    #     plant_id = 'TPP'
    query = PlantProduction.objects.filter(plant=plant_id).order_by('end_reading')
    end_reading = query[len(query) - 1].end_reading
    print(end_reading)
    return HttpResponse(json.dumps(end_reading), content_type='application/json')


class PlantProductionDetailView(DetailView):
    model = PlantProduction
    template_name = 'toris/plant-production-detail.html'
    context_object_name = 'plantdetailall'


class ProductionUpdateView(UpdateView):
    model = PlantProduction
    template_name = 'toris/plant-production-update.html'
    context_object_name = 'production'
    form_class = PlantProductionForm
    success_url = reverse_lazy('toris:production_list')


class ProductionDeleteView(DeleteView):
    model = PlantProduction
    template_name = 'toris/plant-production-delete.html'
    success_url = reverse_lazy('toris:production_list')


class ProductListView(ListView):
    model = Product
    template_name = 'toris/product_list.html'
    context_object_name = 'productall'
    paginate_by = 20

    def get_queryset(self):
        product_list = Product.objects.all().order_by('product_code')
        return product_list


class ProductSortView(ListView):
    model = Product
    template_name = 'toris/product_list.html'
    context_object_name = 'productall'
    paginate_by = 20
    success_url = reverse_lazy('toris:product_list')

    def get_queryset(self, *args, **kwargs):
        product_list = Product.objects.order_by(self.kwargs.get('data'))
        return product_list


class ProductDetailView(DetailView):
    model = Product
    template_name = 'toris/product_detail.html'
    context_object_name = 'productdetail'


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'toris/product_add.html'
    success_url = reverse_lazy('toris:product_list')


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'toris/product_update.html'
    context_object_name = 'product'
    form_class = ProductForm
    success_url = reverse_lazy('toris:product_list')


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'toris/product_delete.html'
    success_url = reverse_lazy('toris:product_list')


class OrderListView(ListView):
    model = Order
    template_name = 'toris/order_list.html'
    context_object_name = 'orderall'
    paginate_by = 20

    def get_queryset(self):
        order_list = Order.objects.all().order_by('order_date')
        return order_list


class OrderSortView(ListView):
    model = Order
    template_name = 'toris/order_list.html'
    context_object_name = 'orderall'
    paginate_by = 9
    success_url = reverse_lazy('toris:order_list')

    def get_queryset(self, *args, **kwargs):
        order_list = Order.objects.order_by(self.kwargs.get('data'))
        return order_list


class OrderDetailView(DetailView):
    model = Order
    template_name = 'toris/order_detail.html'
    context_object_name = 'orderdetail'


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'toris/order_add.html'
    success_url = reverse_lazy('toris:order_list')


class OrderUpdateView(UpdateView):
    model = Order
    template_name = 'toris/order_update.html'
    context_object_name = 'order'
    form_class = OrderForm
    success_url = reverse_lazy('toris:order_list')


class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'toris/order_delete.html'
    success_url = reverse_lazy('toris:order_list')


class ProductionOrderListView(ListView):
    model = Order
    template_name = 'toris/production_order.html'
    context_object_name = 'orders'

    def get_queryset(self):
        # que = Order.objects.all().select_related('product_code')
        product = Product.objects.all()
        order_groupby = Order.objects.values('product_code').annotate(sum_o=Sum('order_qty'))
        production_groupby = PlantProduction.objects.values('product_code').annotate(
            sum_p=Sum(F('end_reading') - F('start_reading')))
        # print(production_groupby.query)
        product = product.values()
        product_df = pd.DataFrame.from_records(product)
        # print(production_groupby)
        # print(order_groupby)
        # print(q)
        order_df = pd.DataFrame(order_groupby)
        production_df = pd.DataFrame(production_groupby)
        production_order = production_df.merge(order_df, left_on='product_code', right_on='product_code',
                                            how='right')

        # production_order = production_order.replace([np.nan], 0)
        production_order['net_p'] = production_order['sum_o']-production_order['sum_p']
        production_order = production_order[['product_code','net_p']]
        # production_order = production_order.astype({'product_code': 'int', 'sum_p': 'float',
        #      'sum_o': 'float', 'net_p': 'float'})
        production_order.reset_index(drop=True)
        production_order =production_order.dropna()
        print(production_order)
        production_order = production_order.merge(product_df, left_on='product_code', right_on='product_code',
                                            how='left')

        production_order = production_order.sort_values(['net_p'])
        production_order=production_order.to_dict('records')
        return production_order
def export_production_order_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="production_order_csv.csv"'
    writer = csv.writer(response)
    writer.writerow(['product_code','required_production', 'tape_color', 'color_marking_on_bobin', 'req_denier', 'req_gramage',
                     'req_tape_width', 'stock_of_bobin','cutter_spacing', 'req_streanth_per_tape_in_kg', 'req_elongation_percent','streanth',
                     'tanacity','pp_percent','filler_percent','shiner_percent','color_percent','tpt_percent',
                     'uv_percent','color_name'])
    product = Product.objects.all()
    order_groupby = Order.objects.values('product_code').annotate(sum_o=Sum('order_qty'))
    production_groupby = PlantProduction.objects.values('product_code').annotate(
        sum_p=Sum(F('end_reading') - F('start_reading')))
    product = product.values()
    product_df = pd.DataFrame.from_records(product)
    order_df = pd.DataFrame(order_groupby)
    production_df = pd.DataFrame(production_groupby)
    production_order = production_df.merge(order_df, left_on='product_code', right_on='product_code',
                                           how='right')
    production_order = production_order.replace([np.nan], 0)
    production_order['net_p'] = production_order['sum_o'] - production_order['sum_p']
    production_order = production_order[['product_code', 'net_p']]
    production_order = production_order.merge(product_df, left_on='product_code', right_on='product_code',
                                              how='left')
    production_order = production_order.sort_values(['net_p'])
    production_order = production_order.values.tolist()
    for item in production_order:
        writer.writerow(item)
    return response





# import pandas as pd
# today = datetime.today().strftime('%Y-%m-%d')
# date1 = pd.to_datetime(today)
# class SearchView(ListView):
#     template_name = 'stockapp/search.html'
#     context_object_name = 'all_search_results'
#     # paginate_by = 9
#
#     def get_queryset(self):
#
#         query = self.request.GET.get('search')
#         if query == 'new_closing_high':
#             postresult= Stock_price.objects.filter(stock_id_id =OuterRef("pk")).filter(date__gte=datetime.today()-timedelta(days=365)).values('stock_id_id').annotate(max_close=Max('close')).order_by('-max_close')
#             postresult1 = Stock.objects.all().annotate( max_close=Subquery(postresult.values('max_close')[:1] ),date =Subquery(postresult.values('date')[:1] ) ).order_by('nse_symbol')
#             postresult2 = postresult1.filter(date = date1.date() )
#             print(postresult2)
#             print(date1.date())
#             result = postresult1
#         else:
#
#            result = Stock.objects.order_by('name')
#         return result
#
#
#

# class ProductListView(ListView):
#     template_name = 'toris/product_list.html'
#     context_object_name = 'productall'
#     # paginate_by = 9
#
#     def get_queryset(self):  # new
#         return Product.objects.order_by('product_code')

# class OrderListView(ListView):
#     template_name = 'toris/order_list.html'
#     context_object_name = 'orderall'
#     # paginate_by = 9
#
#     def get_queryset(self):  # new
#         return Order.objects.order_by('order_date')

# class StockDetailListView(ListView):
#     template_name = 'stockapp/detail.html'
#     context_object_name = 'stocksdetail'
#     paginate_by = 50
#     def get_queryset(self):
#         self.id = get_object_or_404(Stock, id=self.kwargs['id'])
#         stock_obj = Stock_price.objects.order_by('date').filter(stock_id_id=self.id)
#             # .filter(date__year = '2021')
#         return stock_obj
#
#     def get_context_data(self, **kwargs):
#         name = get_object_or_404(Stock, id=self.kwargs['id'])
#         data = super().get_context_data(**kwargs)
#         data['stockname'] = name
#         data['exchange'] = 'NSE'
#         return data
#
#
