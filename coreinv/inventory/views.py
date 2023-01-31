import num2words
from django.db.models import Max, F
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (View, ListView, CreateView, UpdateView, DeleteView, TemplateView, DetailView)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .models import *
from .forms import *
from sales.models import InvoiceItem,Invoice
from purchase.models import PurchaseInvoice,PurchaseInvoiceItem
from django_filters.views import FilterView
from .filters import StockFilter, ProductFilter
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic.dates import YearArchiveView, MonthArchiveView, ArchiveIndexView


class HomeView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = ('inventory.view_stock',)
    template_name = "homepage/home.html"

    def get(self, request):
        inventory = Inventory.objects.all()

        sales = Invoice.objects.order_by('-date')[:3]
        purchases = PurchaseInvoice.objects.order_by('-date')[:3]
        context = {
            'inventory': inventory,
            'sales': sales,
            'purchases': purchases
        }
        return render(request, self.template_name, context)


class AboutView(TemplateView):
    template_name = "homepage/about.html"


class InventoryListView(PermissionRequiredMixin, LoginRequiredMixin, FilterView):
    permission_required = ('inventory.view_inventory',)
    filterset_class = StockFilter
    queryset = Inventory.objects.all().filter(product__is_deleted=False)
    template_name = 'stocks/inventory_list.html'
    paginate_by = 5


class InventoryPurchaseRequiredView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = ('inventory.view_inventory',)
    template_name = 'stocks/purchase_required.html'
    paginate_by = 5

    def get_queryset(self):
        obj = Inventory.objects.all().filter(current_stock__lt=F('alert_level')).annotate(
            purchase_reqd_qty=F('alert_level') - F('current_stock'))
        return obj


class InventoryCreateView(PermissionRequiredMixin, SuccessMessageMixin, LoginRequiredMixin,
                          CreateView):  # createview class to add new stock, mixin used to display message
    permission_required = ('inventory.add_inventory',)
    model = Inventory  # setting 'Stock' model as model
    form_class = InventoryForm  # setting 'StockForm' form as form
    template_name = "stocks/edit_inventory.html"  # 'edit_stock.html' used as the template
    success_url = reverse_lazy(
        'inventory:inventory-list')  # redirects to 'inventory' page in the url after submitting the form
    success_message = "Inventory has been created successfully"  # displays message when form is submitted

    def get_context_data(self, **kwargs):  # used to send additional context
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Inventory'
        context["savebtn"] = 'Add to Inventory'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        """If the form is valid, save the associated model."""
        self.object = form.save()
        return super().form_valid(form)


class InventoryUpdateView(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin,
                          UpdateView):  # updateview class to edit stock, mixin used to display message
    permission_required = ('inventory.change_inventory',)
    model = Inventory  # setting 'Stock' model as model
    form_class = InventoryForm  # setting 'StockForm' form as form
    template_name = "stocks/edit_inventory.html"  # 'edit_stock.html' used as the template
    success_url = reverse_lazy(
        'inventory:inventory-list')  # redirects to 'inventory' page in the url after submitting the form
    success_message = "Inventory has been updated successfully"  # displays message when form is submitted

    def get_context_data(self, **kwargs):  # used to send additional context
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Inventory'
        context["savebtn"] = 'Update Inventory'
        context["delbtn"] = 'Delete Inventory'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        """If the form is valid, save the associated model."""
        self.object = form.save()
        return super().form_valid(form)


class InventoryDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):  # view class to delete stock
    permission_required = ('inventory.delete_inventory',)
    template_name = "stocks/delete_inventory.html"  # 'delete_stock.html' used as the template
    success_message = "Inventory has been deleted successfully"  # displays message when form is submitted
    success_url = reverse_lazy('inventory:inventory-list')
    model = Inventory

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.user = self.request.user
        self.object.soft_delete()
        return HttpResponseRedirect(success_url)


class InventoryLogView(ListView):
    permission_required = ('inventory.view_purchaseinvoiceitem', 'inventory:view_invoiceitem')
    template_name = 'stocks/inventory_logs.html'
    paginate_by = 5

    def get_queryset(self):
        self.product = get_object_or_404(Product, name=self.kwargs['product'])
        return InvoiceItem.objects.filter(product=self.product)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the supplier
        context['inventory'] = Inventory.objects.get(product=self.product)
        context['invoiceitem'] = InvoiceItem.objects.filter(product=self.product)
        context['purchaseinvoiceitem'] = PurchaseInvoiceItem.objects.filter(product=self.product)
        return context


class ProductListView(PermissionRequiredMixin, LoginRequiredMixin, FilterView):
    permission_required = ('inventory.view_product',)
    filterset_class = ProductFilter
    queryset = Product.objects.all()
    template_name = 'products/product_list.html'
    paginate_by = 5


class ProductCreateView(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin,
                        CreateView):  # createview class to add new stock, mixin used to display message
    permission_required = ('inventory.add_product',)

    model = Product  # setting 'Stock' model as model
    form_class = ProductForm  # setting 'StockForm' form as form
    template_name = "products/edit_product.html"  # 'edit_stock.html' used as the template
    # success_url = '/products'  # redirects to 'inventory' page in the url after submitting the form
    success_message = "Product has been created successfully"  # displays message when form is submitted

    def get_context_data(self, **kwargs):  # used to send additional context
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Product'
        context["savebtn"] = 'Add to Product'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        """If the form is valid, save the associated model."""
        self.object = form.save()
        return super().form_valid(form)


class ProductUpdateView(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin,
                        UpdateView):  # updateview class to edit stock, mixin used to display message
    permission_required = ('inventory.change_product',)
    model = Product  # setting 'Stock' model as model
    form_class = ProductForm  # setting 'StockForm' form as form
    template_name = "products/edit_product.html"  # 'edit_stock.html' used as the template
    success_url = reverse_lazy(
        'inventory:product-list')  # redirects to 'inventory' page in the url after submitting the form
    success_message = "Product has been updated successfully"  # displays message when form is submitted

    def get_context_data(self, **kwargs):  # used to send additional context
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Product'
        context["savebtn"] = 'Update Product'
        context["delbtn"] = 'Delete Product'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        """If the form is valid, save the associated model."""
        self.object = form.save()
        return super().form_valid(form)


class ProductDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):  # view class to delete stock
    permission_required = ('inventory.delete_product',)
    template_name = "products/delete_product.html"  # 'delete_stock.html' used as the template
    success_message = "Product has been deleted successfully"  # displays message when form is submitted
    success_url = reverse_lazy('inventory:product-list')
    model = Product

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.user = self.request.user
        self.object.soft_delete()
        return HttpResponseRedirect(success_url)


