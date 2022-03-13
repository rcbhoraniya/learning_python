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
from django_filters.views import FilterView
from .filters import StockFilter, ProductFilter
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from .utils import *
from django.views.generic.dates import YearArchiveView,MonthArchiveView


class HomeView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = ('inventory.view_stock',)
    template_name = "homepage/home.html"

    def get(self, request):
        stock = Stock.objects.all().order_by('-quantity')

        sales = Invoice.objects.order_by('-date')[:3]
        purchases = PurchaseInvoice.objects.order_by('-date')[:3]
        context = {
            'stock': stock,
            'sales': sales,
            'purchases': purchases
        }
        return render(request, self.template_name, context)


class AboutView(TemplateView):
    template_name = "homepage/about.html"


class StockListView(PermissionRequiredMixin, LoginRequiredMixin, FilterView):
    permission_required = ('inventory.view_stock',)
    filterset_class = StockFilter
    queryset = Stock.objects.all().filter(product__is_deleted=False)
    template_name = 'stocks/stock_list.html'
    paginate_by = 5


class StockPurchaseRequiredView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = ('inventory.view_stock',)
    template_name = 'stocks/purchase_required.html'
    paginate_by = 5

    def get_queryset(self):
        obj = Stock.objects.all().filter(quantity__lt=F('alert_level')).annotate(
            purchase_reqd_qty=F('alert_level') - F('quantity'))
        return obj


class StockCreateView(PermissionRequiredMixin, SuccessMessageMixin, LoginRequiredMixin,
                      CreateView):  # createview class to add new stock, mixin used to display message
    permission_required = ('inventory.add_stock',)
    model = Stock  # setting 'Stock' model as model
    form_class = StockForm  # setting 'StockForm' form as form
    template_name = "stocks/edit_stock.html"  # 'edit_stock.html' used as the template
    # success_url = '/stocks'  # redirects to 'inventory' page in the url after submitting the form
    success_message = "Stock has been created successfully"  # displays message when form is submitted

    def get_context_data(self, **kwargs):  # used to send additional context
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Stock'
        context["savebtn"] = 'Add to Inventory'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        """If the form is valid, save the associated model."""
        self.object = form.save()
        return super().form_valid(form)


class StockUpdateView(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin,
                      UpdateView):  # updateview class to edit stock, mixin used to display message
    permission_required = ('inventory.change_stock',)
    model = Stock  # setting 'Stock' model as model
    form_class = StockForm  # setting 'StockForm' form as form
    template_name = "stocks/edit_stock.html"  # 'edit_stock.html' used as the template
    success_url = '/stocks'  # redirects to 'inventory' page in the url after submitting the form
    success_message = "Stock has been updated successfully"  # displays message when form is submitted

    def get_context_data(self, **kwargs):  # used to send additional context
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Stock'
        context["savebtn"] = 'Update Stock'
        context["delbtn"] = 'Delete Stock'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        """If the form is valid, save the associated model."""
        self.object = form.save()
        return super().form_valid(form)


class StockDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):  # view class to delete stock
    permission_required = ('inventory.delete_stock',)
    template_name = "stocks/delete_stock.html"  # 'delete_stock.html' used as the template
    success_message = "Stock has been deleted successfully"  # displays message when form is submitted
    success_url = reverse_lazy('inventory:stock-list')
    model = Stock

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.user = self.request.user
        self.object.soft_delete()
        return HttpResponseRedirect(success_url)


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
    success_url = 'inventory:product-list'  # redirects to 'inventory' page in the url after submitting the form
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


class CustomerListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = ('inventory.view_customer',)
    template_name = "customers/customer_list.html"
    paginate_by = 5

    def get_queryset(self):
        """Return the last five Customer objects."""
        return Customer.objects.all().order_by('name')[:5]


class CustomerCreateView(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = ('inventory.add_customer',)
    model = Customer
    form_class = CustomerForm
    success_url = 'inventory:customer-list'
    success_message = "Customer has been created successfully"
    template_name = "customers/edit_customer.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Customer'
        context["savebtn"] = 'Add Customer'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        """If the form is valid, save the associated model."""
        self.object = form.save()
        return super().form_valid(form)


class CustomerUpdateView(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = ('inventory.change_customer',)
    model = Customer
    form_class = CustomerForm
    success_url = 'inventory:customer-list'
    success_message = "Customer details has been updated successfully"
    template_name = "customers/edit_customer.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Customer'
        context["savebtn"] = 'Save Changes'
        context["delbtn"] = 'Delete Customer'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        """If the form is valid, save the associated model."""
        self.object = form.save()
        return super().form_valid(form)


class CustomerDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('inventory.delete_customer',)
    template_name = "customers/delete_customer.html"
    success_message = "Customer has been deleted successfully"
    model = Customer
    success_url = reverse_lazy('inventory:customer-list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.user = self.request.user
        self.object.soft_delete()
        return HttpResponseRedirect(success_url)


class CustomerBillListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = ('inventory.view_invoice', 'inventory.view_customer',)
    template_name = 'customers/customer_bill_list.html'
    context_object_name = 'customerbills'
    paginate_by = 5

    def get_queryset(self):
        self.customer = get_object_or_404(Customer, name=self.kwargs['name'])
        return Invoice.objects.filter(customer=self.customer)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the customer
        context['customer'] = self.customer
        return context


class SupplierListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = ('inventory.view_supplier',)
    model = Supplier
    template_name = "suppliers/suppliers_list.html"
    queryset = Supplier.objects.all()


class SupplierCreateView(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = ('inventory.add_supplier',)
    model = Supplier
    form_class = SupplierForm
    success_url = 'inventory:supplier-list'
    success_message = "Supplier has been created successfully"
    template_name = "suppliers/edit_supplier.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Supplier'
        context["savebtn"] = 'Add Supplier'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        """If the form is valid, save the associated model."""
        self.object = form.save()
        return super().form_valid(form)


class SupplierUpdateView(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = ('inventory.change_supplier',)
    model = Supplier
    form_class = SupplierForm
    success_url = 'inventory:supplier-list'
    success_message = "Supplier details has been updated successfully"
    template_name = "suppliers/edit_supplier.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Supplier'
        context["savebtn"] = 'Save Changes'
        context["delbtn"] = 'Delete Supplier'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        """If the form is valid, save the associated model."""
        self.object = form.save()
        return super().form_valid(form)


# used to delete a supplier
class SupplierDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('inventory.delete_supplier',)
    template_name = "suppliers/delete_supplier.html"
    success_message = "Supplier has been deleted successfully"
    model = Supplier
    success_url = reverse_lazy('inventory:suppliers-list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.user = self.request.user
        self.object.soft_delete()
        return HttpResponseRedirect(success_url)


# used to view a supplier's profile
class SupplierBillListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = ('inventory.view_purchaseinvoice', 'inventory:view_supplier')
    template_name = 'suppliers/supplier_bill_list.html'
    context_object_name = 'supplierbills'
    paginate_by = 5

    def get_queryset(self):
        self.supplier = get_object_or_404(Supplier, name=self.kwargs['name'])
        return PurchaseInvoice.objects.filter(supplier=self.supplier)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the supplier
        context['supplier'] = self.supplier
        return context


# shows the list of bills of all purchases
class PurchaseBillListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = ('inventory.view_purchaseinvoice',)
    model = PurchaseInvoice
    template_name = "purchases/purchases_bill_list.html"
    context_object_name = 'purchasebills'
    ordering = ['-date']
    paginate_by = 5


class SalseBillListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = ('inventory.view_invoice',)
    model = Invoice
    template_name = "sales/sales_bill_list.html"
    context_object_name = 'salebills'
    ordering = ['-date']
    paginate_by = 5


class SalesBillCreateView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = ('inventory.add_invoice',)
    # template_name = 'sales/salesinvoice_create.html'
    template_name = 'sales/new.html'

    def invoice_data_validate(self, data):
        # Validate Invoice Info ----------
        # invoice-number
        try:
            invoice_number = int(data['invoice-number'])
        except:
            print("Error: Incorrect Invoice Number")
            return "Error: Incorrect Invoice Number"
        # invoice date
        try:
            date_text = data['invoice-date']
            datetime.datetime.strptime(date_text, '%Y-%m-%d')
        except:
            print("Error: Incorrect Invoice Date")
            return "Error: Incorrect Invoice Date"
        # Validate Customer Data ---------
        # customer-name
        if len(data['customer-name']) < 1 or len(data['customer-name']) > 200:
            print("Error: Incorrect Customer Name")
            return "Error: Incorrect Customer Name"
        if len(data['customer-address']) > 250:
            print("Error: Incorrect Customer Address")
            return "Error: Incorrect Customer Address"
        if len(data['customer-city']) > 100:
            print("Error: Incorrect Customer City")
            return "Error: Incorrect Customer City"
        if len(data['customer-phone']) > 14:
            print("Error: Incorrect Customer Phone")
            return "Error: Incorrect Customer Phone"
        if len(data['customer-email']) > 100:
            print("Error: Incorrect Customer email")
            return "Error: Incorrect Customer email"
        if len(data['customer-gst']) != 15 and len(data['customer-gst']) != 0:
            print("Error: Incorrect Customer GST")
            return "Error: Incorrect Customer GST"
        return None

    def customer_data_process(self, data):
        customer_data = {}
        customer_data['id'] = data['customer-id']
        customer_data['name'] = data['customer-name']
        customer_data['address'] = data['customer-address']
        customer_data['city'] = data['customer-city']
        customer_data['email'] = data['customer-email']
        customer_data['phone'] = data['customer-phone']
        customer_data['gstin'] = data['customer-gst']
        return customer_data

    def invoice_data_processor(self, data):
        invoice_data = {}
        invoice_data['invoice_number'] = data['invoice-number']
        invoice_data['date'] = data['invoice-date']
        invoice_data['customer'] = self.customer_data_process(data)
        invoice_data['vehicle_number'] = data['vehicle-number']
        invoice_data['eway_number'] = data['eway-number']
        invoice_data['lr_number'] = data['lr-number']
        invoice_data['po_number'] = data['po-number']
        invoice_data['challan_number'] = data['challan-number']

        if 'igstcheck' in data:
            invoice_data['igstcheck'] = True
        else:
            invoice_data['igstcheck'] = False

        invoice_data['total_amt_with_gst'] = float(data['invoice-total-amt-with-gst'])
        invoice_data['total_amt_without_gst'] = float(
            data['invoice-total-amt-without-gst'])
        invoice_data['total_amt_sgst'] = float(data['invoice-total-amt-sgst'])
        invoice_data['total_amt_cgst'] = float(data['invoice-total-amt-cgst'])
        invoice_data['total_amt_igst'] = float(data['invoice-total-amt-igst'])

        invoice_data['items'] = []
        invoice_post_data = dict(data)
        for idx, product in enumerate(invoice_post_data['invoice-product']):
            if product:
                # print(idx, product)
                item_entry = {}
                item_entry['name'] = product
                item_entry['hsn'] = invoice_post_data['invoice-hsn'][idx]
                item_entry['unit'] = invoice_post_data['invoice-unit'][idx]
                item_entry['quantity'] = int(invoice_post_data['invoice-qty'][idx])
                item_entry['rate_with_gst'] = float(invoice_post_data['invoice-rate-with-gst'][idx])
                item_entry['rate_without_gst'] = float(invoice_post_data['invoice-rate-without-gst'][idx])
                item_entry['gst_percentage'] = float(invoice_post_data['invoice-gst-percentage'][idx])
                item_entry['amt_with_gst'] = float(invoice_post_data['invoice-amt-with-gst'][idx])
                item_entry['amt_without_gst'] = float(invoice_post_data['invoice-amt-without-gst'][idx])
                item_entry['amt_sgst'] = float(invoice_post_data['invoice-amt-sgst'][idx])
                item_entry['amt_cgst'] = float(invoice_post_data['invoice-amt-cgst'][idx])
                item_entry['amt_igst'] = float(invoice_post_data['invoice-amt-igst'][idx])


                invoice_data['items'].append(item_entry)

        # print(processed_invoice_data)
        return invoice_data

    def update_invoiceitem_and_stock(self, invoice_data):
        # invoice_data = json.loads(invoice.invoice_json)
        # invoice_no = invoice.invoice_number
        invoice = Invoice.objects.get(user=self.request.user, invoice_number=invoice_data['invoice_number'], )

        for item in invoice_data['items']:
            product = Product.objects.get(user=self.request.user,
                                          name=item['name'],
                                          hsn=item['hsn'],
                                          unit=item['unit'],
                                          gst_percentage=item['gst_percentage'])
            stock = Stock.objects.get(user=self.request.user, product=product)
            invoiceitem = InvoiceItem(user=self.request.user,
                                      invoice=invoice,
                                      product=product,
                                      quantity=item['quantity'],
                                      rate_with_gst = item['rate_with_gst'],
                                      rate_without_gst=item['rate_without_gst'],
                                      amt_with_gst=item['amt_with_gst'],
                                      amt_without_gst=item['amt_without_gst'],
                                      amt_cgst=item['amt_cgst'],
                                      amt_sgst=item['amt_sgst'],
                                      amt_igst=item['amt_igst'])

            change = int(item['quantity'])

            stock.quantity -= change
            invoiceitem.save()
            stock.save()

    def get(self, request):
        invoiceform = InvoiceForm(request.GET or None)
        customerform = CustomerForm(request.GET or None)
        productform = ProductForm(request.GET or None)
        invoiceitemformset = InvoiceItemFormset(request.GET or None)
        customers = Customer.objects.all()
        products = Product.objects.all()
        default_invoice_number = Invoice.objects.filter(user=request.user).aggregate(Max('invoice_number'))[
            'invoice_number__max']
        if not default_invoice_number:
            default_invoice_number = 1
        else:
            default_invoice_number += 1
        default_invoice_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')

        context = {
            'invoiceform': invoiceform,
            'customerform':customerform,
            'productform':productform,
            'invoiceitemformset':invoiceitemformset,
            # 'customers': customers,
            # 'products': products,
            # 'default_invoice_number': default_invoice_number,
            # 'default_invoice_date': default_invoice_date,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        print("POST received - Invoice Data")
        invoice_data = request.POST
        print(invoice_data)
        validation_error = self.invoice_data_validate(invoice_data)
        if validation_error:
            context["error_message"] = validation_error
            return render(request, 'sales/invoice_create.html', context)

        # valid invoice data
        print("Valid Invoice Data")
        customer_data = self.customer_data_process(invoice_data)
        invoice_data_processed = self.invoice_data_processor(invoice_data)
        # save customer
        customer = None
        try:
            customer = Customer.objects.get(user=request.user,
                                            id=customer_data['id'],
                                            name=customer_data['name'],
                                            email=customer_data['email'],
                                            )


        except:
            print("===============> customer not found============================")
            print(customer_data['name'])
            print(customer_data['id'])
            print(customer_data['address'])
            print(customer_data['phone'])
            print(customer_data['gstin'])

        if not customer:
            print("=============================CREATING CUSTOMER===============>")
            customer = Customer(user=request.user,
                                name=customer_data['name'],
                                address=customer_data['address'],
                                city=customer_data['city'],
                                email=customer_data['email'],
                                phone=customer_data['phone'],
                                gstin=customer_data['gstin'])
            # create customer book
            customer.save()
            # add_customer_book(customer)
        print(customer)
        # # save product
        # update_products_from_invoice(invoice_data_processed, request)
        # # save invoice
        invoice_data_processed_json = json.dumps(invoice_data_processed)
        new_invoice = Invoice(user=request.user,
                              invoice_number=int(invoice_data_processed['invoice_number']),
                              date=datetime.datetime.strptime(invoice_data_processed['date'], '%Y-%m-%d'),
                              customer=customer,
                              invoice_json=invoice_data_processed_json,
                              total_amt_with_gst=invoice_data_processed['total_amt_with_gst'],
                              total_amt_without_gst = invoice_data_processed['total_amt_without_gst'],
                              total_amt_sgst=invoice_data_processed['total_amt_sgst'],
                              total_amt_cgst=invoice_data_processed['total_amt_cgst'],
                              total_amt_igst=invoice_data_processed['total_amt_igst'],
                              igstcheck = invoice_data_processed['igstcheck'],
                              eway_number=invoice_data_processed['eway_number'],
                              lr_number=invoice_data_processed['lr_number'],
                              vehicle_number=invoice_data_processed['vehicle_number'],
                              po_number=invoice_data_processed['po_number'],
                              challan_number=invoice_data_processed['challan_number'], )
        new_invoice.save()
        print("INVOICE SAVED")
        # invoiceitem = InvoiceItem(invoice_number=new_invoice)

        # self.update_invoiceitem_and_stock(new_invoice)
        self.update_invoiceitem_and_stock(invoice_data_processed)
        print("INVENTORY UPDATED")
        #
        # auto_deduct_book_from_invoice(new_invoice)
        # print("CUSTOMER BOOK UPDATED")

        return redirect('inventory:salesbill_viewer', invoice_number=new_invoice.invoice_number)


class SalseBillViewer(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = ('inventory.view_invoiceitem',)
    template_name = 'sales/salesbill_printer.html'
    context_object_name = 'invoiceitem_data'

    def get_queryset(self):
        return InvoiceItem.objects.filter(invoice_id__invoice_number=self.kwargs['invoice_number'])

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        invoice_obj = get_object_or_404(Invoice, user=self.request.user, invoice_number=self.kwargs['invoice_number'])
        user_profile = get_object_or_404(UserProfile, user=self.request.user)

        context['invoice'] = invoice_obj
        context['currency'] = "₹"
        context['total_in_words'] = num2words.num2words(int(invoice_obj.total_amt_with_gst),
                                                        lang='en_IN').title()
        context['user_profile'] = user_profile
        return context



class SalesDeleteView(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = ('inventory.delete_invoice',)
    model = Invoice
    template_name = "sales/delete_sale.html"
    success_url = reverse_lazy('inventory:sales-list')
    success_message = "Sale bill  has been deleted successfully"

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.user = self.request.user
        items = InvoiceItem.objects.filter(invoice=self.object.invoice_number)
        for item in items:
            stock = get_object_or_404(Stock, product=item.product)
            if stock.is_deleted == False:
                stock.quantity += item.quantity
                stock.save()
        self.object.soft_delete()
        return HttpResponseRedirect(success_url)


class PurchaseDeleteView(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = ('inventory.view_purchaseinvoice',)
    model = PurchaseInvoice
    template_name = "purchases/delete_purchase.html"
    success_url = reverse_lazy('inventory:purchases-list')
    success_message = "Purchase bill  has been deleted successfully"

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.user = self.request.user

        items = PurchaseInvoiceItem.objects.filter(purchaseinvoice=self.object.invoice_number)
        for item in items:
            stock = get_object_or_404(Stock, product=item.product)
            if stock.is_deleted == False:
                stock.quantity -= item.quantity
                stock.save()
        self.object.soft_delete()
        return HttpResponseRedirect(success_url)


def customersjson(request):
    customers = list(Customer.objects.all().values())
    return JsonResponse(customers, safe=False)


def suppliersjson(request):
    suppliers = list(Supplier.objects.all().values())
    return JsonResponse(suppliers, safe=False)


def productsjson(request):
    print(request)
    products = list(Product.objects.all().values())
    return JsonResponse(products, safe=False)


def customerjson(request):
    customer = list(Customer.objects.all().filter(id=request.GET.get('customerid')).values())
    return JsonResponse(customer, safe=False)


def productjson(request):
    print("product", request.GET.get('productid'))
    product = list(Product.objects.all().filter(id=request.GET.get('productid')).values())
    print(product)
    return JsonResponse(product, safe=False)


class PurchaseCreateView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = ('inventory.add_purchaseinvoice',)
    template_name = 'purchases/purchaseinvoice_create.html'

    def invoice_data_validate(self, data):
        # Validate Invoice Info ----------
        # invoice-number
        try:
            invoice_number = int(data['invoice-number'])
        except:
            print("Error: Incorrect Invoice Number")
            return "Error: Incorrect Invoice Number"
        # invoice date
        try:
            date_text = data['invoice-date']
            datetime.datetime.strptime(date_text, '%Y-%m-%d')
        except:
            print("Error: Incorrect Invoice Date")
            return "Error: Incorrect Invoice Date"
        # Validate Customer Data ---------
        # customer-name
        if len(data['supplier-name']) < 1 or len(data['supplier-name']) > 200:
            print("Error: Incorrect Supplier Name")
            return "Error: Incorrect Supplier Name"
        if len(data['supplier-address']) > 250:
            print("Error: Incorrect supplier Address")
            return "Error: Incorrect supplier Address"
        if len(data['supplier-city']) > 100:
            print("Error: Incorrect supplier City")
            return "Error: Incorrect supplier City"
        if len(data['supplier-phone']) > 14:
            print("Error: Incorrect supplier Phone")
            return "Error: Incorrect supplier Phone"
        if len(data['supplier-email']) > 100:
            print("Error: Incorrect supplier email")
            return "Error: Incorrect supplier email"
        if len(data['supplier-gst']) != 15 and len(data['supplier-gst']) != 0:
            print("Error: Incorrect supplier GSTIN")
            return "Error: Incorrect supplier GSTIN"
        return None

    def supplier_data_process(self, data):
        supplier_data = {}
        supplier_data['id'] = data['supplier-id']
        supplier_data['name'] = data['supplier-name']
        supplier_data['address'] = data['supplier-address']
        supplier_data['city'] = data['supplier-city']
        supplier_data['email'] = data['supplier-email']
        supplier_data['phone'] = data['supplier-phone']
        supplier_data['gstin'] = data['supplier-gst']
        return supplier_data

    def invoice_data_processor(self, data):
        invoice_data = {}
        invoice_data['invoice_number'] = data['invoice-number']
        invoice_data['date'] = data['invoice-date']
        invoice_data['supplier'] = self.supplier_data_process(data)
        invoice_data['vehicle_number'] = data['vehicle-number']
        invoice_data['eway_number'] = data['eway-number']
        invoice_data['lr_number'] = data['lr-number']
        invoice_data['po_number'] = data['po-number']
        invoice_data['challan_number'] = data['challan-number']

        if 'igstcheck' in data:
            invoice_data['igstcheck'] = True
        else:
            invoice_data['igstcheck'] = False

        invoice_data['items'] = []
        invoice_data['total_amt_with_gst'] = float(data['invoice-total-amt-with-gst'])
        invoice_data['total_amt_without_gst'] = float(data['invoice-total-amt-without-gst'])
        invoice_data['total_amt_sgst'] = float(data['invoice-total-amt-sgst'])
        invoice_data['total_amt_cgst'] = float(data['invoice-total-amt-cgst'])
        invoice_data['total_amt_igst'] = float(data['invoice-total-amt-igst'])

        invoice_post_data = dict(data)
        for idx, product in enumerate(invoice_post_data['invoice-product']):
            if product:
                # print(idx, product)
                item_entry = {}
                item_entry['name'] = product
                item_entry['hsn'] = invoice_post_data['invoice-hsn'][idx]
                item_entry['unit'] = invoice_post_data['invoice-unit'][idx]
                item_entry['quantity'] = int(invoice_post_data['invoice-qty'][idx])
                item_entry['rate_with_gst'] = float(invoice_post_data['invoice-rate-with-gst'][idx])
                item_entry['rate_without_gst'] = float(invoice_post_data['invoice-rate-without-gst'][idx])
                item_entry['amt_with_gst'] = float(invoice_post_data['invoice-amt-with-gst'][idx])
                item_entry['amt_without_gst'] = float(invoice_post_data['invoice-amt-without-gst'][idx])
                item_entry['gst_percentage'] = float(invoice_post_data['invoice-gst-percentage'][idx])
                item_entry['amt_sgst'] = float(invoice_post_data['invoice-amt-sgst'][idx])
                item_entry['amt_cgst'] = float(invoice_post_data['invoice-amt-cgst'][idx])
                item_entry['amt_igst'] = float(invoice_post_data['invoice-amt-igst'][idx])

                invoice_data['items'].append(item_entry)

        # print(processed_invoice_data)
        return invoice_data

    def update_invoiceitem_and_stock(self, invoice_data):
        # invoice_data = json.loads(invoice.invoice_json)
        # invoice_no = invoice.invoice_number
        purchaseinvoice = PurchaseInvoice.objects.get(user = self.request.user,  invoice_number=invoice_data['invoice_number'])

        for item in invoice_data['items']:
            product = Product.objects.get(user=self.request.user,
                                          name=item['name'],
                                          hsn=item['hsn'],
                                          unit=item['unit'],
                                          gst_percentage=item['gst_percentage'])
            try:
                stock = Stock.objects.get(user=self.request.user, product=product)
            except:
                stock = Stock(user=self.request.user,
                              product=product,
                              quantity=0
                              )
            purchaseinvoiceitem = PurchaseInvoiceItem(user=self.request.user,
                                                      purchaseinvoice=purchaseinvoice,
                                                      product=product,
                                                      quantity=item['quantity'],
                                                      rate_with_gst=item['rate_with_gst'],
                                                      rate_without_gst=item['rate_without_gst'],
                                                      amt_with_gst=item['amt_with_gst'],
                                                      amt_without_gst=item['amt_without_gst'],
                                                      amt_cgst=item['amt_cgst'],
                                                      amt_sgst=item['amt_sgst'],
                                                      amt_igst=item['amt_igst'])
            change = float(item['quantity'])

            stock.quantity += change
            purchaseinvoiceitem.save()
            stock.save()

    def get(self, request):
        # forms = CustomerForm(request.GET or None)
        suppliers = Supplier.objects.all()
        products = Product.objects.all()
        # default_invoice_number = Invoice.objects.filter(user=request.user).aggregate(Max('invoice_number'))[
        #     'invoice_number__max']
        # if not default_invoice_number:
        #     default_invoice_number = 1
        # else:
        #     default_invoice_number += 1
        default_invoice_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')

        context = {
            # 'forms': forms,
            'suppliers': suppliers,
            'products': products,
            # 'default_invoice_number': default_invoice_number,
            'default_invoice_date': default_invoice_date,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        print("POST received - Invoice Data")
        invoice_data = request.POST
        # print(invoice_data)
        validation_error = self.invoice_data_validate(invoice_data)
        if validation_error:
            context["error_message"] = validation_error
            return render(request, 'purchases/invoice_create.html', context)

        # valid invoice data
        print("Valid Invoice Data")
        supplier_data = self.supplier_data_process(invoice_data)
        invoice_data_processed = self.invoice_data_processor(invoice_data)
        # save customer
        supplier = None
        try:
            supplier = Supplier.objects.get(user=request.user,
                                            id=supplier_data['id'],
                                            name=supplier_data['name'],
                                            email=supplier_data['email'],
                                            gstin=supplier_data['gstin'])


        except:
            print("===============> customer not found============================")
            print(supplier_data['name'])
            print(supplier_data['id'])
            print(supplier_data['address'])
            print(supplier_data['phone'])
            print(supplier_data['gstin'])

        if not supplier:
            print("=============================CREATING CUSTOMER===============>")
            supplier = Supplier(user=request.user,
                                name=supplier_data['name'],
                                address=supplier_data['address'],
                                city=supplier_data['city'],
                                email=supplier_data['email'],
                                phone=supplier_data['phone'],
                                gstin=supplier_data['gstin'])
            # create customer book
            supplier.save()
            # add_customer_book(customer)
        print(supplier)
        # # save product
        # update_products_from_invoice(invoice_data_processed, request)
        # # save invoice
        invoice_data_processed_json = json.dumps(invoice_data_processed)
        new_purchaseinvoice = PurchaseInvoice(user=request.user,
                                              invoice_number=int(invoice_data_processed['invoice_number']),
                                              date=datetime.datetime.strptime(invoice_data_processed['date'], '%Y-%m-%d'),
                                              supplier=supplier,
                                              invoice_json=invoice_data_processed_json,
                                              total_amt_with_gst=invoice_data_processed['total_amt_with_gst'],
                                              total_amt_without_gst= invoice_data_processed['total_amt_without_gst'],
                                              total_amt_sgst=invoice_data_processed['total_amt_sgst'],
                                              total_amt_cgst=invoice_data_processed['total_amt_cgst'],
                                              total_amt_igst=invoice_data_processed['total_amt_igst'],
                                              igstcheck=invoice_data_processed['igstcheck'],
                                              eway_number=invoice_data_processed['eway_number'],
                                              lr_number=invoice_data_processed['lr_number'],
                                              vehicle_number=invoice_data_processed['vehicle_number'],
                                              po_number=invoice_data_processed['po_number'],
                                              challan_number=invoice_data_processed['challan_number'], )
        new_purchaseinvoice.save()
        print("PURCHASE INVOICE SAVED")
        # purchaseinvoiceitem = PurchaseInvoiceItem(invoice_number=new_purchaseinvoice)
        # self.update_invoiceitem_and_stock(new_purchaseinvoice)

        self.update_invoiceitem_and_stock(invoice_data_processed)
        print(" PURCHASE INVENTORY UPDATED")
        #
        # auto_deduct_book_from_invoice(new_invoice)
        # print("CUSTOMER BOOK UPDATED")

        return redirect('inventory:purchasebill_viewer', purchaseinvoice_number=new_purchaseinvoice.invoice_number)


class PurchaseBillViewer(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = ('inventory.view_purchaseinvoice',)
    template_name = 'purchases/purchasebill_printer.html'
    context_object_name = 'purchaseinvoiceitem_data'

    def get_queryset(self):
        return PurchaseInvoiceItem.objects.filter(purchaseinvoice_id__invoice_number=self.kwargs['purchaseinvoice_number'])

    def get_context_data(self, *, object_list=None, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        invoice_obj = get_object_or_404(PurchaseInvoice, user=self.request.user,
                                        invoice_number=self.kwargs['purchaseinvoice_number'])
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        context['purchaseinvoice'] = invoice_obj
        context['currency'] = "₹"
        context['total_in_words'] = num2words.num2words(int(invoice_obj.total_amt_with_gst),
                                                        lang='en_IN').title()
        context['user_profile'] = user_profile
        return context


class InvoiceYearArchiveView(YearArchiveView):
    queryset = Invoice.objects.all()
    date_field = "date"
    make_object_list = True
    allow_future = True
    template_name = 'archive/invoice_year_archive.html'


class InvoiceMonthArchiveView(MonthArchiveView):
    queryset = Invoice.objects.all()
    date_field = "date"
    allow_future = True
    template_name = 'archive/invoice_month_archive.html'
