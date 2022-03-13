from django import forms
from django.db.models import Max
from django.forms import formset_factory,BaseFormSet

from .models import *

class StockForm(forms.ModelForm):
    # product = forms.CharField(label='Product',widget=forms.TextInput({'class':'form-control'}))
    # quantity = forms.CharField(label='Quantity',widget=forms.TextInput({'class':'form-control'}))
    # alert_level = forms.CharField(label='Alert Level',widget=forms.TextInput({'class':'form-control'}))


    def __init__(self, *args, **kwargs):                                                        # used to set css classes to the various fields
        super().__init__(*args, **kwargs)
        self.fields['product'].widget.attrs.update({'class': 'form-control','type':'text'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control','type':'text', 'min': '0'})
        self.fields['alert_level'].widget.attrs.update({'class': 'form-control','type':'text', 'min': '0'})

    class Meta:
        model = Stock
        fields = ['product', 'quantity','alert_level']


class ProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):                                                        # used to set css classes to the various fields
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control','type':'text'})
        self.fields['hsn'].widget.attrs.update({'class': 'form-control','type':'text'})
        self.fields['unit'].widget.attrs.update({'class': 'form-control','type':'text'})
        self.fields['rate_without_gst'].widget.attrs.update({'class': 'form-control', 'type': 'text'})
        self.fields['profit_margin_percentage'].widget.attrs.update({'class': 'form-control', 'type': 'text'})
        self.fields['gst_percentage'].widget.attrs.update({'class': 'form-control','type':'text'})


    class Meta:
        model = Product
        fields = ['name', 'hsn','unit','rate_without_gst','profit_margin_percentage','gst_percentage']


class SupplierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'class': 'form-control','type':'text', 'pattern': '[a-zA-Z\s]{1,50}', 'title': 'Alphabets and Spaces only',
             'required': 'true'})
        self.fields['address'].widget.attrs.update({'class': 'form-control','type':'text'})
        # self.fields['supplier_state'].widget.attrs.update({'class': 'form-control','type':'text'})
        # self.fields['supplier_district'].widget.attrs.update({'class': 'form-control','type':'text'})
        self.fields['city'].widget.attrs.update({'class': 'form-control','type':'text'})
        self.fields['zip'].widget.attrs.update({'class': 'form-control','type':'text'})
        self.fields['phone'].widget.attrs.update(
            {'class': ' form-control','type':'text', 'maxlength': '10', 'pattern': '[0-9]{10}', 'title': 'Numbers only',
             'required': 'true'})
        self.fields['email'].widget.attrs.update({'class': 'form-control','type':'email'})
        self.fields['gstin'].label = "GSTIN"
        self.fields['gstin'].widget.attrs.update(
            {'class': ' form-control','type':'text', 'maxlength': '15', 'pattern': '[A-Z0-9]{15}',
             'title': 'GSTIN Format Required'})

    class Meta:
        model = Supplier
        fields = ['name', 'city', 'zip', 'phone', 'address', 'email', 'gstin']


class CustomerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update(
            {'class': 'form-control','type':'text', 'required': 'true','placeholder':'Enter customer name'})
        self.fields['address'].widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Enter customer address'})
        # self.fields['customer_state'].widget.attrs.update({'class': 'form-control','type':'text'})
        # self.fields['customer_district'].widget.attrs.update({'class': 'form-control','type':'text'})
        self.fields['city'].widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Enter customer city'})
        self.fields['zip'].widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Enter customer pincode'})
        self.fields['phone'].widget.attrs.update(
            {'class': 'form-control','type':'text', 'maxlength': '10', 'pattern': '[0-9]{10}', 'title': 'Numbers only',
             'required': 'true','placeholder':'Enter customer phone'})
        self.fields['email'].widget.attrs.update({'class': 'form-control','type':'email','placeholder':'Enter customer email'})
        self.fields['gstin'].label = "GSTIN"
        self.fields['gstin'].widget.attrs.update(
            {'class': 'form-control','type':'text', 'maxlength': '15', 'pattern': '[A-Z0-9]{15}',
             'title': 'GSTIN Format Required','placeholder':'Enter customer gstin'})

    class Meta:
        model = Customer
        fields = ['name', 'city', 'zip', 'phone', 'address', 'email', 'gstin']

class DateInput(forms.DateInput):
    input_type = 'date'


class InvoiceForm(forms.ModelForm):
    default_invoice_number = Invoice.objects.aggregate(Max('invoice_number'))[
        'invoice_number__max']
    if not default_invoice_number:
        default_invoice_number = 1
    else:
        default_invoice_number += 1


    default_invoice_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')

    CUSTOMER_CHOICE=[('----','Select Customer')]
    customer_obj = Customer.objects.values_list('id', 'name')

    # PRODUCT_CHOICE.append(('----', 'Select'))
    for customer in customer_obj:
        data = customer
        CUSTOMER_CHOICE.append(data)


    customer_id =forms.ChoiceField( label='Name:',choices = CUSTOMER_CHOICE, widget=forms.Select(attrs={'class': 'form-select'}),)


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.fields['invoice_number'].widget.attrs.update({'class': 'form-control','value':self.default_invoice_number})
        self.fields['date'].widget.attrs.update({'class': 'form-control'})
        self.fields['customer'].queryset = Customer.objects.all()
        self.fields['customer'].widget.attrs.update({'class': 'form-select'})
        self.fields['total_amt_with_gst'].widget.attrs.update({'class': 'form-control','readonly':True})
        self.fields['total_amt_without_gst'].widget.attrs.update({'class': 'form-control','readonly':True})
        self.fields['total_amt_cgst'].widget.attrs.update({'class': 'form-control','readonly':True})
        self.fields['total_amt_sgst'].widget.attrs.update({'class': 'form-control','readonly':True})
        self.fields['total_amt_igst'].widget.attrs.update({'class': 'form-control','readonly':True})
        self.fields['igstcheck'].widget.attrs.update({'class': 'form-check-input igstcheck'})
        self.fields['eway_number'].widget.attrs.update({'class': 'form-control','placeholder':'Enter EWay Number'})
        self.fields['lr_number'].widget.attrs.update({'class': 'form-control','placeholder':'Enter LR Number'})
        self.fields['vehicle_number'].widget.attrs.update({'class': 'form-control','placeholder':'Enter Vehicle Number'})
        self.fields['po_number'].widget.attrs.update({'class': 'form-control','placeholder':'Enter PO Number'})
        self.fields['challan_number'].widget.attrs.update({'class': 'form-control','placeholder':'Enter Challan Number'})


    class Meta:
        model =Invoice
        fields = ['invoice_number','date','customer','total_amt_with_gst','total_amt_without_gst',
                  'total_amt_cgst','total_amt_sgst','total_amt_igst','igstcheck','eway_number',
                  'lr_number','vehicle_number','po_number','challan_number']
        widgets = {'date': DateInput(),}


class InvoiceItemForm(forms.ModelForm):


    hsn=forms.CharField(label='HSN',widget=forms.TextInput(attrs={'class':'form-control setprice hsn','readonly':True}))
    unit=forms.CharField(label='Unit',widget=forms.TextInput(attrs={'class':'form-control setprice unit','readonly':True}))
    gst_percentage=forms.DecimalField(label='Unit',widget=forms.NumberInput (attrs={'class':'form-control setprice gst_percentage','readonly':True}))
    profit_margin_percentage=forms.DecimalField(label='Unit',widget=forms.NumberInput (attrs={'class':'form-control setprice profit_margin_percentage','hidden':True}))
    # rate_without_gst= forms.DecimalField(label='Rate without GST',widget=forms.NumberInput(attrs={'class':'form-control setprice rate_without_gst','readonly':True}))
    # rate_with_gst= forms.DecimalField(label='Rate with GST',widget=forms.NumberInput(attrs={'class':'form-control setprice rate_with_gst','readonly':True}))
    #
    # amt_without_gst = forms.DecimalField(label='Amt without GST',widget=forms.NumberInput(attrs={'class':'form-control setprice amt_without_gst','readonly':True}))
    # amt_sgst= forms.DecimalField(label='Amt SGST',widget=forms.NumberInput(attrs={'class':'form-control setprice amt_sgst','readonly':True}))
    # amt_cgst= forms.DecimalField(label='Amt CGST',widget=forms.NumberInput(attrs={'class':'form-control setprice amt_cgst','readonly':True}))
    # amt_igst= forms.DecimalField(label='Amt IGST',widget=forms.NumberInput(attrs={'class':'form-control setprice amt_igst','readonly':True}))
    # amt_with_gst= forms.DecimalField(label='Amt with GST',widget=forms.NumberInput(attrs={'class':'form-control setprice amt_with_gst','readonly':True}))

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        # self.fields['user'].widget.attrs.update({'class': 'form-control','hidden':True,'value':self.user})
        self.fields['product'].queryset = Product.objects.all()

        self.fields['product'].widget.attrs.update({'class': 'form-select product'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control quantity'})
        self.fields['rate_with_gst'].widget.attrs.update({'class': 'form-control  rate_with_gst','readonly':True})
        self.fields['rate_without_gst'].widget.attrs.update({'class': 'form-control  rate_without_gst','readonly':True})
        self.fields['amt_with_gst'].widget.attrs.update({'class': 'form-control  amt_with_gst','readonly':True})
        self.fields['amt_without_gst'].widget.attrs.update({'class': 'form-control amt_without_gst','readonly':True})
        self.fields['amt_cgst'].widget.attrs.update({'class': 'form-control amt_cgst','readonly':True})
        self.fields['amt_sgst'].widget.attrs.update({'class': 'form-control amt_sgst','readonly':True})
        self.fields['amt_igst'].widget.attrs.update({'class': 'form-control amt_igst','readonly':True})


    class Meta:
        model=InvoiceItem
        fields = ['user','product','quantity','rate_with_gst','rate_without_gst','amt_with_gst',
                  'amt_without_gst','amt_cgst','amt_sgst','amt_igst']


# formset used to render multiple 'SaleItemForm'
InvoiceItemFormset = formset_factory(InvoiceItemForm, extra=4)
# formset = InvoiceItemFormset(form_kwargs={'user': request.user})





# class InvoiceForm(forms.Form):
#
#     CUSTOMER_CHOICE= Customer.objects.values_list('id','name')
#     PRODUCT_CHOICE = Product.objects.values_list('id','name')
#
#     default_invoice_number = Invoice.objects.aggregate(Max('invoice_number'))[
#         'invoice_number__max']
#     if not default_invoice_number:
#         default_invoice_number = 1
#     else:
#         default_invoice_number += 1
#     default_invoice_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
#     # CUSTOMER_CHOICE.append(('----','Select'))
#     # PRODUCT_CHOICE.append(('----', 'Select'))
#     # for customer in customer_obj:
#     #     d_t = (customer.id, customer.name)
#     #     CUSTOMER_CHOICE.append(d_t)
#
#     invoice_number= forms.IntegerField(label='Invoice Number:',required = True,
#                                        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Invoice Number','value':default_invoice_number}),)
#
#     invoice_date=forms.DateField(required=True,label='Date:', widget=DateInput(attrs={'class': 'form-control','value':default_invoice_date}) )
#
#     igstcheck=forms.BooleanField(label='IGST:',widget=forms.CheckboxInput(attrs={'class':'form-check-input'}),required=False)
#
#     customer_id =forms.ChoiceField( label='Name:',
#                                         choices = CUSTOMER_CHOICE,
#                                         widget=forms.Select(attrs={'class': 'form-control'}),)
#
#
#     customer_address = forms.CharField( label='Address',widget= forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter Customer Address','readonly':True}))
#     customer_city = forms.CharField(label='City:',widget= forms.TextInput(attrs= {'class':'form-control','placeholder': 'Enter Customer City','readonly':True}))
#     customer_gstin = forms.CharField(label='GSTIN:',widget=forms.TextInput(attrs= {'class':'form-control','placeholder': 'Enter Customer GSTIN','readonly':True}))
#     customer_phone = forms.IntegerField(label='Mobile No:',widget=forms.NumberInput(attrs= {'class':'form-control','placeholder': 'Enter Customer Mobile'}))
#     customer_email = forms.EmailField(label='Email:',widget=forms.EmailInput(attrs= {'class':'form-control','placeholder': 'Enter Customer E-mail'}))
#     customer_name = forms.CharField(widget=forms.HiddenInput())
#
#
#     eway_number = forms.CharField(required = False, label='Eway No:',widget= forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter E-way Number'}))
#     vehicle_number = forms.CharField(required = False, label='Vehicle No:',widget= forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter Vehicle Number'}))
#     po_number = forms.CharField(required = False, label='PO Number:',widget= forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter PO Number'}))
#     lr_number = forms.CharField(required = False, label='LR No',widget= forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter LR Number'}))
#     challan_number = forms.CharField(required = False, label='Challan No:',widget= forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter Challan Number'}))
#
#
#
#     product_name = forms.ChoiceField( choices=PRODUCT_CHOICE,
#                                       widget=forms.Select(attrs={'class': 'form-control product_search_area product_search_input'}) )
#
#     product_hsn = forms.CharField(label='HSN:',widget= forms.TextInput(attrs= {'class':'form-control','placeholder': 'HSN','readonly':True}))
#     product_unit = forms.CharField(label='Unit:',widget= forms.TextInput(attrs= {'class':'form-control','placeholder': 'Unit','readonly':True}))
#     product_quantity = forms.DecimalField(label='Qty',widget=forms.NumberInput(attrs={'class':'form-control'}))
#     product_gst_percentage = forms.DecimalField(label='GST%',widget=forms.NumberInput(attrs={'class':'form-control'}))
#     product_sale_rate_with_gst = forms.DecimalField(label='Rate with GST',widget=forms.NumberInput(attrs={'class':'form-control'}))
#     product_sale_rate_without_gst = forms.DecimalField(label='Rate without GST',widget=forms.NumberInput(attrs={'class':'form-control'}))
#     product_purchase_rate_without_gst = forms.DecimalField(widget=forms.HiddenInput())
#     product_profit_margin_percentage = forms.DecimalField(widget=forms.HiddenInput())
#
#     product_amt_without_gst = forms.DecimalField(label='Amt without GST',widget=forms.NumberInput(attrs={'class':'form-control'}))
#     product_amt_sgst= forms.DecimalField(label='Amt SGST',widget=forms.NumberInput(attrs={'class':'form-control'}))
#     product_amt_cgst= forms.DecimalField(label='Amt CGST',widget=forms.NumberInput(attrs={'class':'form-control'}))
#     product_amt_igst= forms.DecimalField(label='Amt IGST',widget=forms.NumberInput(attrs={'class':'form-control'}))
#     product_amt_with_gst= forms.DecimalField(label='Amt with GST',widget=forms.NumberInput(attrs={'class':'form-control'}))
#
#     product_total_amt_sgst = forms.DecimalField(label='Total SGST',widget=forms.NumberInput(attrs={'class':'form-control'}))
#     product_total_amt_cgst = forms.DecimalField(label='Total CGST',widget=forms.NumberInput(attrs={'class':'form-control'}))
#     product_total_amt_igst = forms.DecimalField(label='Total IGST',widget=forms.NumberInput(attrs={'class':'form-control'}))
#
#     product_total_amt_with_gst = forms.DecimalField(label='Total',widget=forms.NumberInput(attrs={'class':'form-control'}))
#     product_total_amt_without_gst = forms.DecimalField(label='Total without gst',widget=forms.NumberInput(attrs={'class':'form-control'}))





# form used to select a supplier
# class PurchaseCreateForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['billno'].widget.attrs.update({'class': 'form-control','id':'billno'})
#         self.fields['supplier'].queryset = Supplier.objects.all()
#         self.fields['supplier'].widget.attrs.update({'class': 'form-control','id':'supplier'})
#         self.fields['date'].widget.attrs.update({'class': 'form-control','id':'date'})
#         self.fields['bill_total'].widget.attrs.update({'class': 'form-control','id':'bill_total'})
#         self.fields['cgst_total'].widget.attrs.update({'class': 'form-control','id':'cgst_total'})
#         self.fields['sgst_total'].widget.attrs.update({'class': 'form-control','id':'sgst_total'})
#         self.fields['igst_total'].widget.attrs.update({'class': 'form-control','id':'igst_total'})
#         self.fields['cess'].widget.attrs.update({'class': 'form-control','id':'cess'})
#         self.fields['eway'].widget.attrs.update({'class': 'form-control','id':'eway'})
#         self.fields['lrno'].widget.attrs.update({'class': 'form-control','id':'lrno'})
#         self.fields['veh'].widget.attrs.update({'class': 'form-control','id':'veh'})
#         self.fields['destination'].widget.attrs.update({'class': 'form-control','id':'destination'})
#         self.fields['po'].widget.attrs.update({'class': 'form-control','id':'po'})
#         self.fields['challanno'].widget.attrs.update({'class': 'form-control','id':'challanno'})
#
#     class Meta:
#         model = PurchaseBill
#         fields = ['supplier']


# form used to render a single stock item form
# class PurchaseItemForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['item'].queryset = Item.objects.all()
#         self.fields['item'].widget.attrs.update({'class': 'form-control','id':'item', 'required': 'true'})
#         self.fields['quantity'].widget.attrs.update(
#             {'class': 'form-control','id':'quantity', 'min': '0', 'required': 'true'})
#         self.fields['perprice'].widget.attrs.update(
#             {'class': 'form-control', 'min': '0', 'required': 'true' ,'id':'perprice'})
#         self.fields['cgst'].widget.attrs.update({'class': 'form-control','id':'cgst', 'required': 'true'})
#         self.fields['sgst'].widget.attrs.update({'class': 'form-control','id':'sgst', 'required': 'true'})
#         self.fields['igst'].widget.attrs.update({'class': 'form-control','id':'igst', 'required': 'true'})
#
#     class Meta:
#         model = PurchaseItem
#         fields = ['item', 'quantity', 'perprice','cgst','sgst','igst']
#

# formset used to render multiple 'PurchaseItemForm'
# PurchaseItemFormset = formset_factory(PurchaseItemForm, extra=1)


# form used to accept the other details for purchase bill
# class PurchaseDetailsForm(forms.ModelForm):
#     class Meta:
#         model = PurchaseBillDetails
#         fields = ['eway', 'veh', 'destination', 'po', 'cgst', 'sgst', 'igst', 'cess', 'tcs', 'total']
#

# form used for supplier

# class SelectCustomerForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['customer'].queryset = Customer.objects.all()
#         self.fields['customer'].widget.attrs.update({'class': 'form-control'})
#
#     class Meta:
#         model = SaleBill
#         fields = ['customer']


# form used to get customer details
# class SaleForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['customer'].queryset = Customer.objects.all()
#         self.fields['customer'].widget.attrs.update({'class': 'form-control'})
#
#     class Meta:
#         model = SaleBill
#         fields = ['customer']


# form used to render a single stock item form
# class SaleItemForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['stock'].queryset = Stock.objects.filter(is_deleted=False)
#         self.fields['stock'].widget.attrs.update({'class': 'form-control stock', 'required': 'true'})
#         self.fields['quantity'].widget.attrs.update(
#             {'class': 'form-control  quantity', 'min': '0', 'required': 'true'})
#         self.fields['perprice'].widget.attrs.update(
#             {'class': 'form-control  price', 'min': '0', 'required': 'true'})
#
#     class Meta:
#         model = SaleItem
#         fields = ['stock', 'quantity', 'perprice']


# formset used to render multiple 'SaleItemForm'
# SaleItemFormset = formset_factory(SaleItemForm, extra=1)


# form used to accept the other details for sales bill
# class SaleDetailsForm(forms.ModelForm):
#
#
#     class Meta:
#         model = SaleBillDetails
#         fields = ['eway', 'veh', 'destination', 'po', 'cgst', 'sgst', 'igst', 'cess', 'tcs', 'total']
