import json, csv
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, RedirectView
from .models import Product, PlantProduction, Order, Operator
from django.http import HttpResponse, request
from .forms import PlantProductionForm, ProductForm, OrderForm, OperatorForm
from django.db.models import Avg, Max, Min, Sum, Count, F
import pandas as pd
import numpy as np
from django.shortcuts import redirect
from .tables import PlantProductionTable, ProductTable, OrderTable, OperatorTable
from .filters import PlantProductionFilter, ProductFilter, OrderFilter, OperatorFilter
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin, MultiTableMixin
from django_tables2.export.views import ExportMixin
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import *
from django.contrib.auth.forms import *
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator

pd.set_option('display.width', 1500)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 50)


class HomeView(TemplateView):
    template_name = 'toris/home.html'


class PermissionDeniedView(TemplateView):
    template_name = 'toris/permission_denied.html'


class UserAccessMixin(PermissionRequiredMixin, LoginRequiredMixin):

    # def __init__(self, *args: object):
    #     super().__init__(args)
    #     self.request = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())
        if not self.has_permission():

            return redirect('toris:permissiondenied')
        return super(UserAccessMixin, self).dispatch(request, *args, **kwargs)


class UserRegistrationView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'toris/registration.html'
    success_url = reverse_lazy('toris:login')





@method_decorator(login_required(login_url='toris:login', redirect_field_name='next'), name='dispatch')
class PlantProductionListView(ExportMixin, SingleTableMixin, FilterView, ):
    model = PlantProduction
    table_class = PlantProductionTable
    template_name = 'toris/plant-production-list.html'
    filterset_class = PlantProductionFilter
    table_pagination = {"per_page": 100}
    export_formats = ['xlsx', 'csv']
    export_name = 'Plant Production'

    def get_queryset(self):
        # qs = self.model.plantmanager.tpf_day().annotate(production_in_kg=(F('end_reading') - F('start_reading')))
        qs = self.model.objects.all().annotate(production_in_kg=(F('end_reading') - F('start_reading'))).order_by(
            'date', 'end_reading')
        filtered_list = PlantProductionFilter(self.request.GET, queryset=qs)
        return filtered_list.qs
    # def get_context_data(self, **kwargs):
    #
    #     context = super(PlantProductionListView, self).get_context_data(**kwargs)
    #     # f = PlantProductionFilter(self.request.GET, queryset=self.model.objects.all())
    #     # has_filter = field in self.request.GET
    #     context['has_filter'] = 'has_filter'
    #     return context


@method_decorator(login_required(login_url='toris:login', redirect_field_name='next'), name='dispatch')
class ProductListView(ExportMixin, SingleTableMixin, FilterView, ):
    model = Product
    table_class = ProductTable
    template_name = 'toris/product_list.html'
    filterset_class = ProductFilter
    table_pagination = {"per_page": 20}
    export_formats = ['xlsx', 'csv']
    export_name = 'Product'

    def get_queryset(self):
        qs = self.model.objects.all().order_by('product_code')
        filtered_list = ProductFilter(self.request.GET, queryset=qs)
        return filtered_list.qs


@method_decorator(login_required(login_url='toris:login', redirect_field_name='next'), name='dispatch')
class OrderListView(ExportMixin, SingleTableMixin, FilterView, ):
    model = Order
    table_class = OrderTable
    template_name = 'toris/order_list.html'
    filterset_class = OrderFilter
    table_pagination = {"per_page": 20}
    export_formats = ['xlsx', 'csv']
    export_name = 'Order'

    def get_queryset(self):
        qs = self.model.objects.all().order_by('order_date')
        filtered_list = ProductFilter(self.request.GET, queryset=qs)
        return filtered_list.qs


@method_decorator(login_required(login_url='toris:login', redirect_field_name='next'), name='dispatch')
class OperatorListView(ExportMixin, SingleTableMixin, FilterView, ):
    model = Operator
    table_class = OperatorTable
    template_name = 'toris/operator_list.html'
    filterset_class = OperatorFilter
    table_pagination = {"per_page": 10}
    export_formats = ['xlsx', 'csv']
    export_name = 'Operator'

    def get_queryset(self):
        qs = self.model.objects.all()
        filtered_list = OperatorFilter(self.request.GET, queryset=qs)
        return filtered_list.qs


class PlantProductionCreateView(UserAccessMixin, CreateView):
    raise_exception = True
    permission_required = 'toris.add_plantproduction'
    permission_denied_message = 'No permission'
    login_url = 'toris:login'
    redirect_field_name = 'next'

    model = PlantProduction
    form_class = PlantProductionForm
    template_name = 'toris/plant-production-add.html'
    success_url = reverse_lazy('toris:production_list')




class ProductCreateView(UserAccessMixin, CreateView):
    raise_exception = False
    permission_required = ('toris.add_production',)
    permission_denied_message = 'Not Authorise'
    login_url = 'toris:login'
    redirect_field_name = 'next'

    model = Product
    form_class = ProductForm
    template_name = 'toris/product_add.html'
    success_url = reverse_lazy('toris:product_list')


class OrderCreateView(UserAccessMixin, CreateView):
    raise_exception = False
    permission_required = ('toris.add_order',)
    permission_denied_message = 'Not Authorise'
    login_url = 'toris:login'
    redirect_field_name = 'next'

    model = Order
    form_class = OrderForm
    template_name = 'toris/order_add.html'
    success_url = reverse_lazy('toris:order_list')


class OperatorCreateView(UserAccessMixin, CreateView):
    raise_exception = False
    permission_required = ('toris.add_operator',)
    permission_denied_message = 'Not Authorise'
    login_url = 'toris:login'
    redirect_field_name = 'next'

    model = Operator
    form_class = OperatorForm
    template_name = 'toris/operator_add.html'
    success_url = reverse_lazy('toris:operator_list')


class PlantProductionDetailView(UserAccessMixin, DetailView):
    raise_exception = False
    permission_required = ('toris.view_plantproduction',)
    permission_denied_message = 'Not Authorise'
    login_url = 'toris:login'
    redirect_field_name = 'next'

    model = PlantProduction
    template_name = 'toris/plant-production-detail.html'
    context_object_name = 'plantdetailall'

    def get_queryset(self):
        return PlantProduction.objects.all().select_related("product_code")


class ProductDetailView(UserAccessMixin, DetailView):
    raise_exception = False
    permission_required = ('toris.view_product',)
    permission_denied_message = 'Not Authorise'
    login_url = 'toris:login'
    redirect_field_name = 'next'

    model = Product
    template_name = 'toris/product_detail.html'
    context_object_name = 'productdetail'


class OrderDetailView(UserAccessMixin, DetailView):
    raise_exception = False
    permission_required = ('toris.view_order',)
    permission_denied_message = 'Not Authorise'
    login_url = 'toris:login'
    redirect_field_name = 'next'

    model = Order
    template_name = 'toris/order_detail.html'
    context_object_name = 'orderdetail'


class OperatorDetailView(UserAccessMixin, DetailView):
    raise_exception = False
    permission_required = ('toris.view_operator',)
    permission_denied_message = 'Not Authorise'
    login_url = 'toris:login'
    redirect_field_name = 'next'

    model = Operator
    template_name = 'toris/operator_detail.html'
    context_object_name = 'operatordetail'


class ProductionUpdateView(UserAccessMixin, UpdateView):
    raise_exception = False
    permission_required = ('toris.change_plantproduction',)
    permission_denied_message = 'Not Authorise'
    login_url = 'toris:login'
    redirect_field_name = 'next'

    model = PlantProduction
    template_name = 'toris/plant-production-update.html'
    context_object_name = 'production'
    form_class = PlantProductionForm
    success_url = reverse_lazy('toris:production_list')


class ProductUpdateView(UserAccessMixin, UpdateView):
    raise_exception = False
    permission_required = ('toris.change_product',)
    permission_denied_message = 'Not Authorise'
    login_url = 'toris:login'
    redirect_field_name = 'next'

    model = Product
    template_name = 'toris/product_update.html'
    context_object_name = 'product'
    form_class = ProductForm
    success_url = reverse_lazy('toris:product_list')


class OrderUpdateView(UserAccessMixin, UpdateView):
    raise_exception = False
    permission_required = ('toris.change_order',)
    permission_denied_message = 'Not Authorise'
    login_url = 'toris:login'
    redirect_field_name = 'next'

    model = Order
    template_name = 'toris/order_update.html'
    context_object_name = 'order'
    form_class = OrderForm
    success_url = reverse_lazy('toris:order_list')


class OperatorUpdateView(UserAccessMixin, UpdateView):
    raise_exception = False
    permission_required = ('toris.change_operator',)
    permission_denied_message = 'Not Authorise'
    login_url = 'toris:login'
    redirect_field_name = 'next'

    model = Operator
    template_name = 'toris/operator_update.html'
    context_object_name = 'operator'
    form_class = OperatorForm
    success_url = reverse_lazy('toris:operator_list')


class ProductionDeleteView(UserAccessMixin, DeleteView):
    raise_exception = False
    permission_required = ('toris.delete_plantproduction',)
    permission_denied_message = 'Not Authorise'
    login_url = 'toris:login'
    redirect_field_name = 'next'

    model = PlantProduction
    template_name = 'toris/plant-production-delete.html'
    success_url = reverse_lazy('toris:production_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        return HttpResponseRedirect(self.get_success_url())


class ProductDeleteView(UserAccessMixin, DeleteView):
    raise_exception = False
    permission_required = ('toris.delete_product',)
    permission_denied_message = 'Not Authorise'
    login_url = 'toris:login'
    redirect_field_name = 'next'

    model = Product
    template_name = 'toris/product_delete.html'
    success_url = reverse_lazy('toris:product_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        return HttpResponseRedirect(self.get_success_url())


class OrderDeleteView(UserAccessMixin, DeleteView):
    raise_exception = False
    permission_required = ('toris.delete_order',)
    permission_denied_message = 'Not Authorise'
    login_url = 'toris:login'
    redirect_field_name = 'next'

    model = Order
    template_name = 'toris/order_delete.html'
    success_url = reverse_lazy('toris:order_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        return HttpResponseRedirect(self.get_success_url())


class OperatorDeleteView(UserAccessMixin, DeleteView):
    raise_exception = False
    permission_required = ('toris.delete_operator',)
    permission_denied_message = 'Not Authorise'
    login_url = 'toris:login'
    redirect_field_name = 'next'

    model = Operator
    template_name = 'toris/operator_delete.html'
    success_url = reverse_lazy('toris:operator_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required(login_url='toris:login', redirect_field_name='next'), name='dispatch')
class ProductionOrderListView(ListView):
    template_name = 'toris/production_order.html'
    context_object_name = 'production_orders'

    def get_queryset(self):
        product = Product.objects.all()
        order_groupby = Order.objects.values('product_code').annotate(sum_o=Sum('order_qty'))
        production_groupby = PlantProduction.objects.values('product_code').annotate(
            sum_p=Sum(F('end_reading') - F('start_reading')))
        product = product.values()
        product_df = pd.DataFrame.from_records(product)
        order_df = pd.DataFrame(order_groupby)
        production_df = pd.DataFrame(production_groupby)
        production_order = production_df.merge(order_df, left_on='product_code', right_on='product_code',
                                               how='outer')
        production_order = production_order.replace([np.nan], 0)
        production_order['net_p'] = production_order['sum_o'] - production_order['sum_p']
        production_order = production_order[['product_code', 'net_p']]
        production_order = production_order.merge(product_df, left_on='product_code', right_on='product_code',
                                                  how='left')
        production_order = production_order.sort_values(['product_code'])
        production_order = production_order[production_order['net_p'] != 0]
        production_order = production_order.drop(columns=['id', 'is_deleted', 'deleted_at'])
        production_order = production_order.to_dict('records')
        return production_order


def export_production_order_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="production_order_csv.csv"'
    writer = csv.writer(response)
    writer.writerow(
        ['product_code', 'required_production', 'tape_color', 'color_marking_on_bobin', 'denier', 'gramage',
         'tape_width', 'stock_of_bobin', 'cutter_spacing', 'streanth_per_tape_in_kg', 'elongation_percent',
         'tanacity', 'pp_percent', 'filler_percent', 'shiner_percent', 'color_percent', 'tpt_percent',
         'uv_percent', 'color_name'])
    product = Product.objects.all()
    order_groupby = Order.objects.values('product_code').annotate(sum_o=Sum('order_qty'))
    production_groupby = PlantProduction.objects.values('product_code').annotate(
        sum_p=Sum(F('end_reading') - F('start_reading')))
    product = product.values()
    product_df = pd.DataFrame.from_records(product)
    order_df = pd.DataFrame(order_groupby)
    production_df = pd.DataFrame(production_groupby)
    production_order = production_df.merge(order_df, left_on='product_code', right_on='product_code',
                                           how='outer')
    production_order = production_order.replace([np.nan], 0)
    production_order['net_p'] = production_order['sum_o'] - production_order['sum_p']
    production_order = production_order[['product_code', 'net_p']]
    production_order = production_order.merge(product_df, left_on='product_code', right_on='product_code',
                                              how='left')
    production_order = production_order.sort_values(['product_code'])
    production_order = production_order[production_order['net_p'] != 0]
    production_order = production_order.drop(columns=['id', 'is_deleted', 'deleted_at'])
    # print(production_order)
    production_order = production_order.values.tolist()
    for item in production_order:
        writer.writerow(item)
    return response


def load_start_reading(request):
    plant_id = request.GET.get('plant')
    query = PlantProduction.objects.filter(plant=plant_id).order_by('end_reading').last()
    # print(query)
    end_reading = query.end_reading
    # print(end_reading)
    return HttpResponse(json.dumps(end_reading), content_type='application/json')
